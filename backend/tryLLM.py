import asyncio

import llm

answer = asyncio.run(llm.complete("Describe the film Inception in one spoiler-free sentence."))
print(answer)