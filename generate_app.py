import os
from pathlib import Path
import zipfile
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()

def get_user_inputs():
    app_type = input("Enter the type of application (e.g., web, CLI, etc.): ")
    main_language = input("Enter the main programming language (e.g., Python, JavaScript): ")
    features = input("Describe the features you want in the application: ")
    return app_type, main_language, features

def generate_code(app_type, main_language, features):
    prompt = f"Create a {app_type} application using {main_language} with the following features: {features}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1500,
        top_p=1
    )
    
    return response.choices[0].message.content.strip()

def create_app_structure(base_dir, code):
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Determine the file extension based on the main language
    file_extension = ".py" if "python" in main_language.lower() else ".js"
    main_file_path = base_path / f"main{file_extension}"
    
    main_file_path.write_text(code)

def package_application(base_dir, zip_name):
    base_path = Path(base_dir)
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in base_path.rglob('*'):
            zipf.write(file, file.relative_to(base_path))

def main():
    load_dotenv()  # Load environment variables from .env file
    
    global main_language  # Make it global so it can be accessed in create_app_structure
    app_type, main_language, features = get_user_inputs()
    
    code = generate_code(app_type, main_language, features)
    
    base_dir = "generated_app"
    create_app_structure(base_dir, code)
    
    zip_name = "generated_app.zip"
    package_application(base_dir, zip_name)
    
    print(f"Application has been generated and packaged into {zip_name}")

if __name__ == "__main__":
    main()