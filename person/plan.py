from prompt_template.run_gpt_prompt import run_gpt_prompt_wake_up_hour, run_gpt_prompt_daily_plan

def generate_wake_up_hour(persona):
  """
  Generates the time when the persona wakes up. This becomes an integral part
  of our process for generating the persona's daily plan.

  Persona state: identity stable set, lifestyle, first_name

  INPUT:
    persona: The Persona class instance
  OUTPUT:
    an integer signifying the persona's wake up hour
  EXAMPLE OUTPUT:
    8
  """
  # if debug: print ("GNS FUNCTION: <generate_wake_up_hour>")
  return int(run_gpt_prompt_wake_up_hour(persona)[0])


def generate_first_daily_plan(persona, wake_up_hour):
  """
  Generates the daily plan for the persona.
  Basically the long term planning that spans a day. Returns a list of actions
  that the persona will take today. Usually comes in the following form:
  'wake up and complete the morning routine at 6:00 am',
  'eat breakfast at 7:00 am',..
  Note that the actions come without a period.

  Persona state: identity stable set, lifestyle, cur_data_str, first_name

  INPUT:
    persona: The Persona class instance
    wake_up_hour: an integer that indicates when the hour the persona wakes up
                  (e.g., 8)
  OUTPUT:
    a list of daily actions in broad strokes.
  EXAMPLE OUTPUT:
    ['wake up and complete the morning routine at 6:00 am',
     'have breakfast and brush teeth at 6:30 am',
     'work on painting project from 8:00 am to 12:00 pm',
     'have lunch at 12:00 pm',
     'take a break and watch TV from 2:00 pm to 4:00 pm',
     'work on painting project from 4:00 pm to 6:00 pm',
     'have dinner at 6:00 pm', 'watch TV from 7:00 pm to 8:00 pm']
  """
  # if debug: print ("GNS FUNCTION: <generate_first_daily_plan>")
  return run_gpt_prompt_daily_plan(persona, wake_up_hour)[0]

def plan(persona, maze, personas, new_day, retrieved):
  """
  Main cognitive function of the chain. It takes the retrieved memory and
  perception, as well as the maze and the first day state to conduct both
  the long term and short term planning for the persona.

  INPUT:
    maze: Current <Maze> instance of the world.
    personas: A dictionary that contains all persona names as keys, and the
              Persona instance as values.
    new_day: This can take one of the three values.
      1) <Boolean> False -- It is not a "new day" cycle (if it is, we would
         need to call the long term planning sequence for the persona).
      2) <String> "First day" -- It is literally the start of a simulation,
         so not only is it a new day, but also it is the first day.
      2) <String> "New day" -- It is a new day.
    retrieved: dictionary of dictionary. The first layer specifies an event,
               while the latter layer specifies the "curr_event", "events",
               and "thoughts" that are relevant.
  OUTPUT
    The target action address of the persona (persona.scratch.act_address).
  """
  # PART 1: Generate the hourly schedule.
  wake_up_hour = generate_wake_up_hour(persona)
  persona.scratch.daily_req = generate_first_daily_plan(persona, wake_up_hour)
