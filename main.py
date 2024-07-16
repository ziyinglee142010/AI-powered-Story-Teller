import streamlit as st
from openai import OpenAI

api_key = st.secrets['OPENAI_SECRET']
client=OpenAI(api_key=api_key)

content= "You are a bestseller story writer.You will take user's prompt and generate a 1000 words short story for adults age 20-30"

def create_story(content,prompt):
  story_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": 'system',
        "content": content
        },
        {
            "role": "user",
            "content": f'{prompt}',

        }],
    max_tokens = 400,
    temperature= 0.8
  )

  story = story_response.choices[0].message.content
  return story

def refine_image(story):
  design_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": 'system',
        "content": 'Based on the story given.You will design a detailed image prompt for the cover image of this story.THe image prompt should include the theme of the story with relevant color, suitable for adults.The output should be within 100 characters.'
        },
        {
            "role": "user",
            "content": f'{story}',

        }],
    max_tokens = 400,
    temperature= 0.8
  )
  design_prompt = design_response.choices[0].message.content
  return design_prompt

def get_image(design_prompt):
  cover_response=client.images.generate(
    model='dall-e-3',
    prompt = f"{design_prompt} in anime style",
    size = "1024x1024",
    quality = 'standard',
    n=1
  )
  image_url = cover_response.data[0].url
  return image_url

st.title("Story Creator with Image Prompt Generator")
st.subheader("Generate a story based on keywords and create a cover image prompt.")

with st.form('my_form'):
  st.write('Keywords:')
  msg = st.text_input(label='Please enter the keywords to generate your story:')
  submitted = st.form_submit_button(label='Generate Story')

if submitted:
  story = create_story(content,msg)
  st.write("**Generated Story:**")
  st.write(story)

  # Generate the image prompt
  refined_prompt = refine_image(story)
  image_url= get_image(refined_prompt)
  st.write("**Generated Image Prompt:**")
  st.write(refined_prompt)
  st.image(image_url)