---
title: "Notes from my workshop on AI agents"
date: 2026-10-30
description: "What I covered in a workshop for faculty and staff in our college on setting up an AI agent: how it differs from the chat window, the commands that work in both the app and the terminal, how to set up a folder and a short rules file for a task you repeat, a literature folder as the example, and how to check the output."
tags: [AI Weekly, AI agents, research workflow]
faq:
  - q: "What is the difference between an AI chat app and an AI agent?"
    a: "A chat app only sees what you paste into it, one question at a time. An agent works inside a folder on your computer. It reads the files there, writes new files, handles a task with several steps, and asks before it changes anything."
  - q: "What is a good first task for an AI agent?"
    a: "A task you repeat, where the inputs are already in files and you would read the output carefully anyway. Turning a folder of papers or reports into short notes and a comparison table is a good first one. Student records, personnel files, data you don't own, and anything shared in confidence stay out of the folder."
---
In September I gave a workshop for faculty and staff in our college on setting up an AI agent. Most people in the room had used ChatGPT or Claude in the chat window but not the agent that comes with the same app. The setup takes about fifteen minutes and there is no coding, so I thought it was worth an hour. Here is the short version.

## What it is

A chat app only sees what you paste into it. You ask one question and get one answer. An agent works inside a folder on your computer. You pick the folder, it reads the files in it, writes new files, and asks you before it changes anything. That is the whole difference, but it matters, because now it can do a task with several steps and several files instead of one question at a time.

Both of the big apps have one. In the Claude desktop app it is the Code tab at the top. For ChatGPT it is the Codex app. You click "Select folder," pick a folder, and type what you want in plain English. When it wants to write or change a file it asks, and you click approve or deny.

I use the terminal version myself. It is the same agent without the app window: you open a terminal, go to the folder, and type `claude` (or `codex`). Everything else works the same way in the app and in the terminal, including the commands you type at the prompt. The ones I use most in Claude (Codex has the same commands under slightly different names, for example `/new` instead of `/clear` and `/status` instead of `/cost`):

- `/model` picks the model. In the app there is also a dropdown next to Send.
- `/effort low`, `/effort medium`, or `/effort high` sets how hard it thinks. Low is fine for a tracker, high for anything you will read closely.
- `/clear` starts a new task with an empty history.
- `/compact` shrinks the history when a long conversation starts to slow down.
- `/cost` shows what the session has used so far.
- `/resume` picks up an earlier session.

To leave, close the window or type `exit`.

## What to do with it

The example I will use here is a literature folder. For every project I have a folder of papers I need to read, and I always plan to write a short note on each one and a table comparing them. I rarely get to it. This is a good first task for an agent because the inputs are already in files and I would read the output carefully anyway.

Set up the folder first. Put the PDFs in one subfolder. Put the current draft of your paper, or a one-page description if there is no draft yet, in another, so the agent knows what "relevant to my paper" means. Make an empty folder for the output. Then write a short rules file at the top. Claude reads it as CLAUDE.md and Codex reads it as AGENTS.md. Mine for this task has five rules:

1. One note per paper, same headings every time: question, data, method, main finding, relation to my paper.
2. Every fact has to come from a page in the PDF. If it doesn't, write [VERIFY].
3. No upgrades. "Associated with" stays "associated with." A working paper is not "published."
4. One summary table across all papers, with the sample period and the unit of observation.
5. Don't touch anything in the draft folder.

Then the prompt is short, because the rules are already in the folder. Something like: "Read every PDF in the papers folder and write the notes and the table described in CLAUDE.md. Do one paper first and stop so I can check it."

Check the first note against the PDF. If the headings are right and the page references hold, tell it to do the rest. If something is off, fix the rules file, not the prompt. That way the fix is still there next time.

A few things I told the group that apply to any task. Put the rules in the rules file so you don't retype them. Keep the source files short; it reads a two-page summary much better than a sixty-page report. Do one before you do all of them. Start a new conversation (`/clear`) when you switch tasks. And use a cheaper model for the routine parts (the table) and the best model for the parts that need judgment (the notes).

## Where it goes wrong

Sometimes the agent reads a paper badly and writes a confident note anyway. A better prompt won't fix that. The only thing that does is reading the output against the source, which is the step people skip because the output looks finished. For this task I check five things: open the PDF next to the note and make sure each page reference holds; resolve or delete anything still marked [VERIFY]; look for places where "associated with" turned into "causes"; make sure the sample period in the table is the one in the paper; and read the "relation to my paper" paragraph to make sure it is about my paper and not one the model made up for me.

For the workshop I planted a few traps in the demo files, facts that were almost right where the obvious upgrade was wrong, and we checked afterward whether the agent fell in. I would do the same in your own folder. If it doesn't fall in, you learn something about the model. If it does, you learn something about how carefully you proofread.

Some files should never go in the folder: student records or grades, personnel files, data you don't own, and anything shared with you in confidence. The agent sees only the folder, so keeping those files out is what keeps them out of the model. Your university's policy on AI tools applies on top of that.

The rule I ended the workshop with: the agent drafts, you read every line, you send. It saves the typing, not the reading. If you want to try it this week, pick one small task you repeat, give it one folder, and check the first output before you ask for the rest.
