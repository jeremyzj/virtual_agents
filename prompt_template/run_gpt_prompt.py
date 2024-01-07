from gpt import safe_generate_response
from print_prompt import print_run_prompts

def run_gpt_prompt_wake_up_hour(persona, test_input=None, verbose=False):
  """
  Given the persona, returns an integer that indicates the hour when the
  persona wakes up.

  INPUT:
    persona: The Persona class instance
  OUTPUT:
    integer for the wake up hour.
  """
  def create_prompt_input(persona, test_input=None):
    if test_input: return test_input
    prompt_input = [persona.scratch.get_str_iss(),
                    persona.scratch.get_str_lifestyle(),
                    persona.scratch.get_str_firstname()]
    return prompt_input

  def __func_clean_up(gpt_response, prompt=""):
    cr = int(gpt_response.strip().lower().split("am")[0])
    return cr

  def __func_validate(gpt_response, prompt=""):
    try: __func_clean_up(gpt_response, prompt="")
    except: return False
    return True

  def get_fail_safe():
    fs = 8
    return fs

  gpt_param = {"engine": "text-davinci-002", "max_tokens": 5,
             "temperature": 0.8, "top_p": 1, "stream": False,
             "frequency_penalty": 0, "presence_penalty": 0, "stop": ["\n"]}
  prompt_template = "persona/prompt_template/v2/wake_up_hour_v1.txt"
  prompt_input = create_prompt_input(persona, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)
  fail_safe = get_fail_safe()

  output = safe_generate_response(prompt, gpt_param, 5, fail_safe,
                                   __func_validate, __func_clean_up)

  # if debug or verbose:
  print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]

def run_gpt_prompt_daily_plan(persona,
                              wake_up_hour,
                              test_input=None,
                              verbose=False):
  """
  Basically the long term planning that spans a day. Returns a list of actions
  that the persona will take today. Usually comes in the following form:
  'wake up and complete the morning routine at 6:00 am',
  'eat breakfast at 7:00 am',..
  Note that the actions come without a period.

  INPUT:
    persona: The Persona class instance
  OUTPUT:
    a list of daily actions in broad strokes.
  """
  def create_prompt_input(persona, wake_up_hour, test_input=None):
    if test_input: return test_input
    prompt_input = []
    prompt_input += [persona.scratch.get_str_iss()]
    prompt_input += [persona.scratch.get_str_lifestyle()]
    prompt_input += [persona.scratch.get_str_curr_date_str()]
    prompt_input += [persona.scratch.get_str_firstname()]
    prompt_input += [f"{str(wake_up_hour)}:00 am"]
    return prompt_input

  def __func_clean_up(gpt_response, prompt=""):
    cr = []
    _cr = gpt_response.split(")")
    for i in _cr:
      if i[-1].isdigit():
        i = i[:-1].strip()
        if i[-1] == "." or i[-1] == ",":
          cr += [i[:-1].strip()]
    return cr

  def __func_validate(gpt_response, prompt=""):
    try: __func_clean_up(gpt_response, prompt="")
    except:
      return False
    return True

  def get_fail_safe():
    fs = ['wake up and complete the morning routine at 6:00 am',
          'eat breakfast at 7:00 am',
          'read a book from 8:00 am to 12:00 pm',
          'have lunch at 12:00 pm',
          'take a nap from 1:00 pm to 4:00 pm',
          'relax and watch TV from 7:00 pm to 8:00 pm',
          'go to bed at 11:00 pm']
    return fs



  gpt_param = {"engine": "text-davinci-003", "max_tokens": 500,
               "temperature": 1, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}
  prompt_template = "persona/prompt_template/v2/daily_planning_v6.txt"
  prompt_input = create_prompt_input(persona, wake_up_hour, test_input)
  prompt = generate_prompt(prompt_input, prompt_template)
  fail_safe = get_fail_safe()

  output = safe_generate_response(prompt, gpt_param, 5, fail_safe,
                                   __func_validate, __func_clean_up)
  output = ([f"wake up and complete the morning routine at {wake_up_hour}:00 am"]
              + output)

  # if debug or verbose:
  print_run_prompts(prompt_template, persona, gpt_param,
                      prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]


def generate_prompt(curr_input, prompt_lib_file):
  """
  Takes in the current input (e.g. comment that you want to classifiy) and
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this
  function replaces this substr with the actual curr_input to produce the
  final promopt that will be sent to the GPT3 server.
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file.
  RETURNS:
    a str prompt that will be sent to OpenAI's GPT server.
  """
  if type(curr_input) == type("string"):
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt:
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()
