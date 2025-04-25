import google.generativeai as genai
genai.configure(api_key="AIzaSyCXt_3R563rc4Blaec6xXl4m0II9QhGB8w")
model = genai.GenerativeModel("gemini-1.5-flash")
print(model.generate_content("Hello").text)