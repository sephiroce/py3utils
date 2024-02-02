#NeMo to onnx

import nemo
import nemo.collections.asr as nemo_asr
model = nemo_asr.models.ASRModel.from_pretrained("stt_en_conformer_transducer_small")
model.eval()
model.to('cuda')
model.export('mymodel.onnx', onnx_opset_version=10)

import onnx
import onnx_tf
onnx_model = onnx.load('encoder-mymodel.onnx')
tf_model = onnx_tf.backend.prepare(onnx_model)
tf_model.export_graph("encoder-mymodel.tf")
onnx_model = onnx.load('decoder_joint-mymodel.onnx')
tf_model = onnx_tf.backend.prepare(onnx_model)
tf_model.export_graph("decoder_joint-mymodel.tf")

import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_saved_model("encoder-mymodel.tf")
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS,
  tf.lite.OpsSet.SELECT_TF_OPS
]
tflite_model = converter.convert()
open('encoder-mymodel-32bit.tflite', 'wb').write(tflite_model)

converter = tf.lite.TFLiteConverter.from_saved_model("decoder_joint-mymodel.tf")
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS,
  tf.lite.OpsSet.SELECT_TF_OPS
]
tflite_model = converter.convert()
open("decoder_joint-mymodel-32bit.tflite", "wb").write(tflite_model)

converter = tf.lite.TFLiteConverter.from_saved_model("encoder-mymodel.tf")
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS,
  tf.lite.OpsSet.SELECT_TF_OPS
]
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
open('encoder-mymodel-8bit.tflite', 'wb').write(tflite_model)

converter = tf.lite.TFLiteConverter.from_saved_model("decoder_joint-mymodel.tf")
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS,
  tf.lite.OpsSet.SELECT_TF_OPS
]
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
open("decoder_joint-mymodel-8bit.tflite", "wb").write(tflite_model)

