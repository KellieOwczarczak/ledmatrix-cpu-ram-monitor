# Framework 16 Ledmatrix CPU and RAM Monitors 

This is a Python script that I have put together with the help of Claude to display CPU and RAM useage on my Framework 16's ledmatrix modules. The tweaks I made are based on how I like to keep things organized. 

## Verify Your ledmatix Modules 

This assumes that you have the inputmodule installed.

##### note: I have my system setup so that ```python``` is an alias for ```python3``` make the change if your system requrires ```python3```. 

```
python -m pip install --user framework16-inputmodule
```

For more information, visit the Framework Github site: 
https://github.com/FrameworkComputer/inputmodule-rs/blob/main/python/README.md 

## Directory and File Setup

In the process, I created two directories in my $HOME directory:

``` 
mkdir .ledmatrix 
```
This is where I keep the python script and copies of the systemd service scripts. If you change this, you will need to make the appropriate adjustments in the python script and two systemd service scripts.

I also created another directory for the service scripts.

```
mkir -p .config/systemd/user
```
To this second directory copy over the systemd service files.

```
cp .ledmatrix/ledmatrix-* .config/systemd/user/
```
This will copy both of the .service files.

## Starting the Systemd Services

Now that the systemd files are in the necessary directories, it is time to get the systemd services up and running.

```
systemctl --user daemon-reload
systemctl --user enable --now ledmatrix-cpu.service
systemctl --user enable --now ledmatrix-ram.service
```
Now, the systemd service should be running. You can check.

```
systemctl --user  status ledmatrix-cpu.service
systemctl --user  status ledmatrix-ram.service
```
