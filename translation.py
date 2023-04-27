from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='auto', target='ru').translate("Hello everyone! I am Tim")

print(translated)