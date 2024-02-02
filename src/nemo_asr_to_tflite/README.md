# NeMo to TF Lite
- This is on-going task and anything has not been confirmed.
- Our first target is ```stt_en_conformer_transducer_small```.

## references
- loading nemo model: https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/intro.html
- exporting to onnx: https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/core/export.html
- converting to tflite: https://medium.com/@zergtant/convert-pytorch-model-to-tf-lite-with-onnx-tf-232a3894657c

## How to install packages
- install packages the below and place ```convert_nemo2tflite.py``` to ```$NeMo_path```
  ```
  pip install Cython
  pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
  pip install -r requirements/requirements.txt
  pip install -r requirements/requirements_asr.txt
  pip install -r requirements/requirements_lightning.txt
  pip install -r requirements/requirements_common.txt
  pip install -r requirements/requirements_docs.txt
  pip install tensorflow
  pip install tensorflow_probability
  pip install onnx_tf

  git clone https://github.com/NVIDIA/NeMo.git
  ```
- then ```python convert_nemo2tflite.py```
- Why are the size of 8-bit models not quarter the size of 32-bit models?
  ```
  6.3M decoder_joint-mymodel-32bit.tflite
  4.0M decoder_joint-mymodel-8bit.tflite
  6.3M decoder_joint-mymodel.onnx
  4.0K decoder_joint-mymodel.tf
   61M encoder-mymodel-32bit.tflite
   23M encoder-mymodel-8bit.tflite
   57M encoder-mymodel.onnx
  4.0K encoder-mymodel.tf
  ```

## Environment
- ubuntu version: Ubuntu 22.04.3 LTS, WSL2
- cuda: ```NVIDIA-SMI 535.54.04              Driver Version: 536.23       CUDA Version: 12.2```
- nemo : commit id 5fdd12e9a9711b241023eb4ed0922733d69ded5e
- python version: 3.10.12
  ```
  numpy                         1.26.3
  pytorch-lightning             2.0.7
  torch                         2.1.2+cu121
  torchaudio                    2.1.2+cu121
  torchmetrics                  1.3.0.post0
  torchvision                   0.16.2+cu121
  tensorflow                    2.15.0.post1
  tensorflow-addons             0.23.0
  tensorflow-estimator          2.15.0
  tensorflow-io-gcs-filesystem  0.35.0
  tensorflow-probability        0.23.0
  ```



