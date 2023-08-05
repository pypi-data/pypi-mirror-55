# PyChoices
A very small Python library for receiving choice input from your user.

## Installing
```bash
pip3 install pychoices
```

## Quickstart
```python
import pychoices

result = pychoices.ask("Squirtle", "Charmander", "Bulbasaur", label="Choose your Starter!")

print(result)
#(0, "Squirtle") or (1, "Charmander") or (2, "Bulbasaur")
```

## What It Does
PyChoices will clean the terminal and display the options provided in the args.\
The user can change the answer by using the up and down arrows.\
Then, by pressing enter, the option will be defined as selected and the function will finish by returning a tuple.

## Reference
<i>function</i> ask(*args, **kwargs)
> args is the array of choices available for the user.
> kwargs is a dictionary of options for customizing the ask function, the available options are:
>> * <b>label</b>: a string that will be printed along with the choices
>> * <b>color</b>: one of the options in the COLORS class, will be the color of the current activated option.

<i>class</i> Colors
>  Class holding some constant values of colors and styles for using in the ask function, the available colors are:
>>* <b>HEADER</b>: Purple
>>* <b>OKBLUE</b>: Blue
>>* <b>OKGREEN</b>: Green
>>* <b>WARNING</b>: Yellow
>>* <b>FAIL</b>: Red
>>* <b>BOLD</b>: Bold
>>* <b>UNDERLINE</b>: Underlined