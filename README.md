CryoTheraPy
==========


## Installation
Install Miniconda: 
https://docs.anaconda.com/free/miniconda/ 
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
Enable execution of the script:
```
chmod 755 Miniconda3-latest-Linux-x86_64.sh
```
```
./Miniconda3-latest-Linux-x86_64.sh -b -p ./conda3.
```

Source the respective python

Pip install requirements (see Requirements.txt).

Modify shebang to respective python version (which python to see abs path; #![abs. path]).


## Documentation
Move to the docs directory.
To create the documentation:
```
make html
```
will write the html files into the _build directory.

To remove the currently existing documentation:
```
make clean
```

## ML installation
Build and source new conda

Install CUDA 11.8 using conda:
```
conda install nvidia/label/cuda-11.8.0::cuda-toolkit
```

Install PyTorch using pip:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Install FastAI using conda:
```
conda install -c fastai fastai
```

Re-install PyTorch using pip + --ignore-installed and --no-cache-dir:
```
pip3 install --ignore-installed torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
```

Install Timm using pip:
```
pip install timm
```

Install seaborn using conda:
```
conda install seaborn 
```

Install sklearn using conda:
```
conda install sklearn
```