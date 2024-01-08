import json
import datetime
from tools.file import check_if_file_exists

class Scratch:
  def __init__(self, f_saved):

    # WORLD INFORMATION
    # Perceived world time.
    self.curr_time = None
    # Current x,y tile coordinate of the persona.
    self.curr_tile = None
    # Perceived world daily requirement.
    self.daily_plan_req = None

    # THE CORE IDENTITY OF THE PERSONA
    # Base information about the persona.
    self.name = None
    self.first_name = None
    self.last_name = None
    self.age = None
    # L0 permanent core traits.
    self.innate = None
    # L1 stable traits.
    self.learned = None
    # L2 external implementation.
    self.currently = None
    self.lifestyle = None
    self.daily_req = []

    if check_if_file_exists(f_saved): 
      # If we have a bootstrap file, load that here. 
      scratch_load = json.load(open(f_saved))
      if scratch_load["curr_time"] is not None: 
        self.curr_time = datetime.datetime.strptime(scratch_load["curr_time"],
                                                  "%B %d, %Y, %H:%M:%S")
      else: 
        self.curr_time = None
      self.curr_tile = scratch_load["curr_tile"]
      self.daily_plan_req = scratch_load["daily_plan_req"]

      self.name = scratch_load["name"]
      self.first_name = scratch_load["first_name"]
      self.last_name = scratch_load["last_name"]
      self.age = scratch_load["age"]
      self.innate = scratch_load["innate"]
      self.learned = scratch_load["learned"]
      self.currently = scratch_load["currently"]
      self.lifestyle = scratch_load["lifestyle"]
      self.daily_req = scratch_load["daily_req"]

  def get_str_iss(self):
    """
    ISS stands for "identity stable set." This describes the commonset summary
    of this persona -- basically, the bare minimum description of the persona
    that gets used in almost all prompts that need to call on the persona.

    INPUT
      None
    OUTPUT
      the identity stable set summary of the persona in a string form.
    EXAMPLE STR OUTPUT
      "Name: Dolores Heitmiller
       Age: 28
       Innate traits: hard-edged, independent, loyal
       Learned traits: Dolores is a painter who wants live quietly and paint
         while enjoying her everyday life.
       Currently: Dolores is preparing for her first solo show. She mostly
         works from home.
       Lifestyle: Dolores goes to bed around 11pm, sleeps for 7 hours, eats
         dinner around 6pm.
       Daily plan requirement: Dolores is planning to stay at home all day and
         never go out."
    """
    commonset = ""
    commonset += f"Name: {self.name}\n"
    commonset += f"Age: {self.age}\n"
    commonset += f"Innate traits: {self.innate}\n"
    commonset += f"Learned traits: {self.learned}\n"
    commonset += f"Currently: {self.currently}\n"
    commonset += f"Lifestyle: {self.lifestyle}\n"
    commonset += f"Daily plan requirement: {self.daily_plan_req}\n"
    if self.curr_time is not None:
      commonset += f"Current Date: {self.curr_time.strftime('%A %B %d')}\n"
    return commonset

  def get_str_lifestyle(self):
    return self.lifestyle

  def get_str_firstname(self):
    return self.first_name


  def get_str_curr_date_str(self): 
    return self.curr_time.strftime("%A %B %d")
