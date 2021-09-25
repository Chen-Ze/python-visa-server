# Lab Program

:warning: **See [Chen-Ze/lab](https://github.com/Chen-Ze/lab) for configuration procedures and instructions.**
:warning: **The following are outdated.**

## Configuration

The whole program is only tested on Windows. However, with GPIB drivers installed, it should run on Mac and Linux as well.

The configuration procedure should be done on a computer that has Internet access.

1. Make sure that the following are installed on your your computer already:
     1. Python 3: I've only tested it with [Python 3.8.10](https://www.python.org/downloads/release/python-3810/). It should work with newer versions of Python as well.
        - Test it with `python --version` in your command line. Make sure it is Python 3.
     1. [Node.js](https://nodejs.org/en/download/): Tested on Node.js 13 and 14. It should work with newer versions as well.
        - Test it with `node --version` in your command line. Make sure it is newer than `13.x.x`.
     1. [Git](https://git-scm.com/).
        - Test it with `git --version` in your command line. No specific version requirement here.
   1. [Chrome](https://www.google.com/intl/en_sg/chrome/): The graphical user interface should work in Firefox or Safari as well. I have only tested it on Chrome, though.
      - Technically speaking, graphical user interface is not necessary on the computer connected to the instruments. The computer only hosts the web service, which is accessible by other computers in the same LAN.
   1. GPIB drivers: It is provided by National Instrument on Windows. There ar e counterparts on Mac and Linux, although I have not tested.
1. Open the command line on your computer. Go to the directory `/path/to/parent` where you want to put the whole program. The following commands runs on Windows as well as on Unix-like systems.
1. Configure [python-visa-server](https://github.com/Chen-Ze/python-visa-server):
   1. In `/path/to/parent`, run `git clone https://github.com/Chen-Ze/python-visa-server`.
   1. `cd python-visa-server`
   1. If LightField is required, substitute `pi_lightfield.py` (currently empty) with the one that implements the interfaces. The script is not done by me and therefore I am not including it in this repository. Contact me for more information.
      1. Then, in `/path/to/parent/python-visa-server` run `git add .`.
      1. `git commit -m"LightField"`
   1. `cd ..`
1. Configure [lab-server](https://github.com/Chen-Ze/lab-server):
   1. In `/path/to/parent`, run `git clone https://github.com/Chen-Ze/lab-server`.
   1. `cd lab-server`
   1. `npm i`
   1. `npm run build`
   1. `cd ..`
1. Configure [lab-client](https://github.com/Chen-Ze/lab-client):
   1. In `/path/to/parent`, run `git clone https://github.com/Chen-Ze/lab-client`.
   1. `cd lab-client`
   1. `npm i`, which may take around 10~20 mins.
   1. `npm run build`, which may take a few minutes.
   1. `cd ..`

## Updating

- Update `python-visa-server`:
  1. In `/path/to/parent/python-visa-server` run `git pull`.

- Update `lab-server`:
  1. In `/path/to/parent/lab-server` run `git pull`.
  2. `npm i`
  3. `npm run build`
- Update `lab-client`:
  1. In `/path/to/parent/lab-client` run `git pull`.
  2. `npm i`
  3. `npm run build`

## Starting

Running the program requires no Internet connection.

1. In `/path/to/parent/python-visa-server`, run `python http_control.py`.
   - You may create a script in this directory so that the command could be done by a double-click.
   - You don't have to wait until this script exits. It runs during the whole experiment.
   - I will call this process _HTTP CONTROL_ hereafter.
   - You should close (or kill) this process if it is already there before you start it.
2. In `/path/to/parent/lab-server`, run `node .`.
   - You may create a script in this directory so that the command could be done by a double-click.
   - You don't have to wait until this script exits. It runs during the whole experiment.
   - I will call this process _LAB SERVER_ hereafter.
   - You should close (or kill) this process if it is already there before you start it.
3. You don't have to do anything with `/path/to/parent/lab-client`.
4. Open Chrome and go to `localhost` in the address bar.
5. (_Optional_) Access the graphical interface using a remote computer:
   1. Make sure that both computers are in the same LAN.
   2. Find out the IP address of the computer running the server.
   3. In the web browser (ideally Chrome) of the remote computer, go to the IP address of the server.
   4. **Warning:** To access LightField, you may have to connect using a remote desktop.

## Doing Experiments

### Experiment from Scratch

1. Type the full path to the file that you want to save your data in the _Save data to_ textbox.
2. For each instrument you want to use (Keithley 2400, Keithley 2600, etc), click the _ADD INSTRUMENT_ button.
   - Specify a unique and semantic name to each instrument in the _Name_ textbox, like Gate or Tunneling.
   - Select the address to the instrument in the _Address_ selection box. If the address of your target instrument does not turn up, it is probably the problem with the driver. Check, for example, from NI MAX if the address shows up there.
   - Select the correct prototype from the _Prototype_ selection box. The default value is GPIB, but you should select a more specific option.
3. Add columns to store experiment data.
   1. From the bottom bar, find and click the _Data_ tab to open it.
   2. In the textbox with a plus button, type the label of the column and click the plus button or hit `<Enter>` to add a column.
   3. Add all the columns you want before starting the experiment.
4. Now you may move the cursor to the _Plus_ button in the main panel and add some experiments. Experiments may be nested under the _Subsequence_ tab.
5. (_Optional_) Add plots.
   1. From the bottom bar, find and click the _Plot_ tab to open it.
   2. Move the cursor to the _Plus_ button the lower right corner of the _Plot_ tab. A menu should pop up.
   3. Click _Simple Plot_. This should create a new plot.
   4. In the _X_ textbox, type the expression for the x-axis. Math functions and column names could be used.
   5. In the _Y_ textbox, type the expression for the x-axis. Math functions and column names could be used.
   6. Select column names in the _Slider_ or _Trace_ (or both) selection box if necessary.
6. (_Optional_) Add monitors.
   1. From the bottom bar, find and click the _Monitor_ tab to open it.
   2. Specify a semantic title to each monitor in the _Title_ textbox.
   3. Set the interval between two monitor pollings in the _Delay_ textbox (in milliseconds).
   4. Select the address to the instrument you want to monitor in the _Address_ selection box.
   5. Select the prototype of the instrument in the _Prototype_ selection box.
   6. Click the plus button on the right.
   7. **Warning:** A delay value that is too small may slow down the program. Also note that monitor does polling to the target instrument, which may slow down its measurement. Add a monitor only when you feel it necessary.
7. (_Optional_) Save the experiment sequence. This enables you to rerun the same experiment with the same or different parameters later.
   1. From the bottom bar, find and click the _Sequence_ tab to open it.
   2. Move the cursor to the _Plus_ button the lower right corner of the _Sequence_ tab. A menu should pop up.
   3. Click _Save_. The sequence, instruments, label of columns, plots, and monitors will be saved. However, experiment data will not be saved in this way even if you save after the experiment is done.
8. Start the experiment by clicking the start button on the top bar.
9. After the experiment ended, close (or kill) _HTTP CONTROL_ and _LAB SERVER_.

### Experiment from Saved Sequence

1. Import the experiment.
   1. From the bottom bar, find and click the _Sequence_ tab to open it.
   2. Move the cursor to the _Plus_ button the lower right corner of the _Sequence_ tab. A menu should pop up.
   3. Click _Import_ and select the sequence file you saved. The sequence, instruments, label of columns, plots, and monitors will be imported.
2. Make necessary modifications.
   1. Make sure that the path in the _Save data to_ text box is correct.
   2. Make sure that the address in all the _Address_ selection boxes are correct. Check the topbar (expand the collapse first) as well the the _Monitor_ tab.
   3. Modify the parameters in the experiments if necessary.
3. Then everything is the same as in _Experiment from Scratch_.

## Troubleshoot

1. You may close (or kill) _HTTP CONTROL_ and _LAB SERVER_ to halt any ongoing experiment.
   - Generally, this will not change the parameters already sent to the instruments.
2. If the experiment does not start after clicking the start button, you may also close (or kill) _HTTP CONTROL_ and _LAB SERVER_ to restart them.
3. Contact the author if you have any problem.

## Contact Me

- Author: Chen Ze
  - Email: chenze_ustc@mail.ustc.edu.cn
