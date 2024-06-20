
import ollama
import variables
data = [
    {
        'role': 'user',
        'content': 'generate a poem on fathers day!'
    },
    {
        'role': 'assistant',
        'content': '''Here's a Father's Day poem:

A hero in every way,
You show us how to seize the day.
With guidance and with gentle care,
You help us grow, without a single snare.

Your love is strong, your heart so true,
A constant presence, through all we do.
From dawn till dusk, from sun to night,
You're there for us, shining bright.

You teach us how to be brave and bold,
To take risks, and never grow old.
With wisdom earned, and a patient ear,
You help us navigate life's every fear.

Your sacrifices, your hard work too,
Are the reasons why our hearts are true blue.
So on this Father's Day, we say,
Thank you for being there, in every way.

From late night talks, to bedtime stories told,
To helping hands, and a heart of gold,
You're the rock that holds us tight,
A father like no other, in all your might.

So here's to you, dear dad of ours,
On this special day, we celebrate yours.
May it be filled with joy and delight,
And many more years of love, shining bright!
'''
    }
]
# client = openai.OpenAI(api_key="blah-blah",base_url="http://localhost:11434/v1")
# name = client.chat.completions.create(model="qwen2:0.5b", stream=False, messages=variables.create_name_prompt(variables.sample))
# print(name.response)
name = ollama.generate(model='qwen2:0.5b',stream=False,system=variables.NAME_PROMPT,prompt=str(data))
print(name['response'])