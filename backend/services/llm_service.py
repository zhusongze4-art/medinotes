import re
import json
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
from models.schemas import ClinicalSummary
from config import LLM_MODEL_NAME, LLM_MAX_NEW_TOKENS, LLM_MAX_RETRIES

logger = logging.getLogger(__name__)


SOAP_PROMPT_TEMPLATE = """<|im_start|>system
You are a clinical documentation assistant. Given a patient-physician dialogue, extract a structured SOAP note.

Respond ONLY with a valid JSON object. No explanation, no markdown, no extra text.

The JSON must match this exact schema:
{{
  "patient_name": "string",
  "age": integer or null,
  "subjective": "patient complaints, symptoms, history",
  "objective": "physical exam findings, test results",
  "assessment": "diagnosis or clinical impression",
  "plan": "treatment plan, follow-up steps",
  "medications": ["list of mentioned medications"],
  "diagnoses": ["list of diagnoses"]
}}
<|im_end|>
<|im_start|>user
{dialogue}
<|im_end|>
<|im_start|>assistant
"""


class LLMService:
    def __init__(self):
        logger.info(f"Loading model: {LLM_MODEL_NAME}")
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype="auto",
            device_map="auto"
        )
        logger.info("Model loaded successfully")

    def _build_prompt(self, dialogue: str) -> str:
        return SOAP_PROMPT_TEMPLATE.format(dialogue=dialogue)

    def _generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=LLM_MAX_NEW_TOKENS,
            do_sample=False,
            temperature=1.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        # 只解码新生成的 token，不包含 prompt 部分
        new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True)

    def _extract_json(self, raw_output: str) -> dict:
        # 尝试找到 JSON 对象的起止位置
        match = re.search(r'\{[\s\S]*\}', raw_output)
        if not match:
            raise ValueError("No JSON object found in LLM output")
        json_str = match.group()
        return json.loads(json_str)

    def generate_summary(self, dialogue: str) -> ClinicalSummary:
        for attempt in range(1, LLM_MAX_RETRIES + 1):
            try:
                prompt = self._build_prompt(dialogue)
                raw_output = self._generate(prompt)
                logger.info(f"Attempt {attempt} raw output: {raw_output[:200]}...")

                parsed = self._extract_json(raw_output)
                summary = ClinicalSummary.model_validate(parsed)

                logger.info(f"Successfully parsed on attempt {attempt}")
                return summary

            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {type(e).__name__}: {e}")
                if attempt == LLM_MAX_RETRIES:
                    raise RuntimeError(
                        f"Failed to generate valid summary after {LLM_MAX_RETRIES} attempts"
                    ) from e