import os
import google.generativeai as genai

class LLMService:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        genai.configure(api_key=api_key)
        # Based on available models for the user
        self.model_name = 'gemini-2.0-flash-exp'
        self.model = genai.GenerativeModel(self.model_name)

    def interpret_hexagram(self, question, cast_result, language='English'):
        """
        Sends the cast result and user question to the LLM for interpretation.
        """
        try:
            return self._generate(question, cast_result, language)
        except Exception as e:
            # ... (fallback logic remains similar, just passing language)
            # For brevity in this edit, assuming fallback also needs update or we just update _generate
            # Let's update the whole method to be safe with the fallback call
            fallback = 'gemini-flash-latest'
            if self.model_name != fallback:
                print(f"Model {self.model_name} failed, trying {fallback}. Error: {e}")
                self.model_name = fallback
                self.model = genai.GenerativeModel(fallback)
                return self._generate(question, cast_result, language)
            raise e

    def _generate(self, question, cast_result, language):
        
        # ... (lines processing code)
        
        lines_desc = []
        moving_lines = []
        for i, val in enumerate(cast_result['raw_values']):
            line_num = i + 1
            if val == 6: 
                desc = "Old Yin (Moving Line) - Yin changing to Yang"
                lines_desc.append(desc)
                moving_lines.append(f"Line {line_num}: {desc}")
            elif val == 7: 
                lines_desc.append("Young Yang (Static Line) - Yang")
            elif val == 8: 
                lines_desc.append("Young Yin (Static Line) - Yin")
            elif val == 9: 
                desc = "Old Yang (Moving Line) - Yang changing to Yin"
                lines_desc.append(desc)
                moving_lines.append(f"Line {line_num}: {desc}")
        
        # Lines are generated bottom to top
        lines_text = "\n".join([f"Line {i+1}: {desc}" for i, desc in enumerate(lines_desc)])
        
        moving_lines_text = "\n".join(moving_lines) if moving_lines else "None"

        prompt = f"""
        You are an expert I Ching master and philosopher. 
        A user has asked the following question: "{question}"
        
        They have cast the following hexagram (lines are listed from bottom to top):
        {lines_text}
        
        Summary of Moving Lines:
        {moving_lines_text}
        
        Please provide a profound and helpful interpretation in {language}. 
        1. Identify the Primary Hexagram.
        2. Identify any Moving Lines and their specific meaning (Only interpret the lines listed in the Summary of Moving Lines).
        3. Identify the Relating (Future) Hexagram if there are moving lines.
        4. Synthesize the answer to directly address the user's question.
        
        Format the output with clear Markdown headings. Use a wise, calming, and insightful tone.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
