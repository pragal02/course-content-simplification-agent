import os
import json
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# ---------------------------------------------------------------------------
# Level-specific instructions injected into the prompt
# ---------------------------------------------------------------------------
LEVEL_INSTRUCTIONS = {
    "Beginner": (
        "The student is a complete beginner with no prior knowledge of this topic. "
        "Use very simple language, everyday analogies, and avoid all jargon. "
        "If a technical term must appear, immediately explain it in plain words."
    ),
    "Intermediate": (
        "The student has basic familiarity with the subject. "
        "Use clear, straightforward language. You may use common technical terms "
        "but briefly clarify any advanced ones. Balance simplicity with accuracy."
    ),
    "Advanced": (
        "The student has strong subject knowledge. "
        "Retain full technical depth and correct domain terminology. "
        "Focus on precision, nuance, and deeper connections between concepts."
    ),
}


def build_prompt(content: str, level: str) -> str:
    level_instruction = LEVEL_INSTRUCTIONS.get(level, LEVEL_INSTRUCTIONS["Intermediate"])

    return f"""You are an expert academic tutor. A student has provided the following course content and wants it simplified for their proficiency level.

Proficiency Level: {level}
Level Instruction: {level_instruction}

Course Content:
\"\"\"{content}\"\"\"

Your task is to process the content above and return a JSON object — no extra text, no markdown fences, just the raw JSON.

The JSON must have exactly these five keys:

1. "simplified_explanation": A clear, cohesive paragraph that re-explains the content at the given proficiency level.
2. "key_points": A JSON array of 4–6 strings, each a concise key takeaway.
3. "important_terms": A JSON array of objects, each with "term" and "meaning" keys. Include 3–5 important terms with plain-language meanings appropriate for the level.
4. "example": A single concrete, relatable example that illustrates the core concept at the given proficiency level.
5. "self_assessment": A JSON array of exactly 3 short questions a student can use to test their understanding.

Respond with only the JSON object. Do not include any explanation outside the JSON.
"""


def simplify_content(content: str, level: str) -> dict:
    """
    Call IBM Granite via watsonx.ai and return the parsed structured response.
    Raises ValueError if the response cannot be parsed or credentials are missing.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    if not api_key or not project_id:
        raise ValueError(
            "WATSONX_API_KEY and WATSONX_PROJECT_ID must be set in your .env file."
        )

    credentials = Credentials(url=url, api_key=api_key)
    client = APIClient(credentials=credentials, project_id=project_id)

    model = ModelInference(
        model_id="ibm/granite-13b-instruct-v2",
        api_client=client,
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 1200,
            GenParams.STOP_SEQUENCES: [],
            GenParams.REPETITION_PENALTY: 1.1,
        },
    )

    prompt = build_prompt(content, level)
    response = model.generate_text(prompt=prompt)

    # Attempt to extract the JSON block from the response
    raw = response.strip()

    # Strip a markdown code fence if the model adds one despite the instruction
    if raw.startswith("```"):
        lines = raw.splitlines()
        # Remove first and last fence lines
        raw = "\n".join(
            line for line in lines
            if not line.strip().startswith("```")
        ).strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Try to find the first { ... } block as a fallback
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            result = json.loads(raw[start:end])
        else:
            raise ValueError(
                "The model returned an unexpected format. "
                "Please try again or rephrase your input."
            )

    # Validate required keys are present
    required = {"simplified_explanation", "key_points", "important_terms", "example", "self_assessment"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Model response is missing fields: {', '.join(missing)}")

    return result
