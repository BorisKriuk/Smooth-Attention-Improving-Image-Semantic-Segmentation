# Smooth-Attention-Improving-Image-Semantic-Segmentation
Code accompaniment for the research work submitted by Sparcus Technologies Limited on Smooth Attention: Improving Image Semantic Segmentation

Preprint can be found here:  https://www.preprints.org/manuscript/202409.1283/v1 <br>

# Abstract <br>
Attention mechanisms have become a fundamental component of deep learning, including the field of computer vision. The key idea behind attention in computer vision is to help the model focus on the relevant spatial regions of the input image, rather than treating all regions equally. The traditional approaches to attention mechanisms in computer vision often suffer from distribution inconsistencies in the attention maps, resulting in sharp transitions that negatively affect model’s focus and lead to poor generalization on complex shapes. The problem of spatial incoherence is particularly pronounced in the task of semantic segmentation, where accurate pixel-level predictions require a detailed understanding of the spatial relationships within the image. In this paper, we propose an attention mechanism called Smooth Attention designed for convolutional neural networks to address the problem of spatial inconsistency in attention maps through multidimensional spatial smoothing. We conduct a series of experiments to evaluate the effectiveness of the proposed mechanism and demonstrate its superior performance compared to traditional methods.

# Data <br>
Caltech-UCSD Birds-200-2011 [1] <br>
Large-Scale Dataset for Segmentation and Classification [2] <br>
Fire Segmentation Image Dataset [3] <br>
Kvasir-Instrument: Diagnostic and Therapeutic Tool Segmentation Dataset in Gastrointestinal Endoscopy [4] <br>
Flood Semantic Segmentation Dataset [5] <br>

[1] Wah, C., Branson, S., Welinder, P., Perona, P., & Belongie, S. (2011). The caltech-ucsd birds-200-2011 dataset. <br>
[2] Ulucan, O., Karakaya, D., & Turkan, M. (2020, October). A large-scale dataset for fish segmentation and classification. In 2020 Innovations in Intelligent Systems and Applications Conference (ASYU) (pp. 1-5). IEEE. <br>
[3] DiversisAI. (n.d.). Fire segmentation image dataset. Kaggle. https://www.kaggle.com/datasets/diversisai/fire-segmentation-image-dataset <br>
[4] Jha, D., Ali, S., Emanuelsen, K., Hicks, S. A., Thambawita, V., Garcia-Ceja, E., Riegler, M. A., de Lange, T., Schmidt, P. T., Johansen, H. D., Johansen, D., & Halvorsen, P. (2021). Kvasir-Instrument: Diagnostic and therapeutic tool segmentation dataset in gastrointestinal endoscopy. In MultiMedia Modeling (pp. 218–229). Springer International Publishing. <br>
[5] Li, H. (n.d.). Flood semantic segmentation dataset. Kaggle. https://www.kaggle.com/datasets/lihuayang111265/flood-semantic-segmentation-dataset <br>


 # Repository Structure <br>
smooth_att_0_1+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.1 threshold. <br>
smooth_att_0_1+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.1 threshold. <br>
smooth_att_0_1+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.1 threshold. <br>
smooth_att_0_1+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.1 threshold. <br>
smooth_att_0_1+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.1 threshold. <br>
<br>
smooth_att_0_2+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.2 threshold. <br>
smooth_att_0_2+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.2 threshold. <br>
smooth_att_0_2+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.2 threshold. <br>
smooth_att_0_2+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.2 threshold. <br>
smooth_att_0_2+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.2 threshold. <br>
<br>
smooth_att_0_3+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.3 threshold. <br>
smooth_att_0_3+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.3 threshold. <br>
smooth_att_0_3+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.3 threshold. <br>
smooth_att_0_3+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.3 threshold. <br>
smooth_att_0_3+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.3 threshold. <br>
<br>
smooth_att_0_4+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.4 threshold. <br>
smooth_att_0_4+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.4 threshold. <br>
smooth_att_0_4+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.4 threshold. <br>
smooth_att_0_4+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.4 threshold. <br>
smooth_att_0_4+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.4 threshold. <br>
<br>
smooth_att_0_5+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.5 threshold. <br>
smooth_att_0_5+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.5 threshold. <br>
smooth_att_0_5+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.5 threshold. <br>
smooth_att_0_5+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.5 threshold. <br>
smooth_att_0_5+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.5 threshold. <br>
<br>
smooth_att_0_6+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.6 threshold. <br>
smooth_att_0_6+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.6 threshold. <br>
smooth_att_0_6+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.6 threshold. <br>
smooth_att_0_6+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.6 threshold. <br>
smooth_att_0_6+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.6 threshold. <br>
<br>
smooth_att_0_7+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.7 threshold. <br>
smooth_att_0_7+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.7 threshold. <br>
smooth_att_0_7+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.7 threshold. <br>
smooth_att_0_7+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.7 threshold. <br>
smooth_att_0_7+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.7 threshold. <br>
<br>
smooth_att_0_8+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.8 threshold. <br>
smooth_att_0_8+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.8 threshold. <br>
smooth_att_0_8+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.8 threshold. <br>
smooth_att_0_8+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.8 threshold. <br>
smooth_att_0_8+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.8 threshold. <br>
<br>
smooth_att_0_9+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 0.9 threshold. <br>
smooth_att_0_9+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 0.9 threshold. <br>
smooth_att_0_9+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 0.9 threshold. <br>
smooth_att_0_9+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 0.9 threshold. <br>
smooth_att_0_9+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 0.9 threshold. <br>
<br>
smooth_att_2+cub_200.py: Code for Smooth Attention module implementation for CUB-200 Dataset at 2 threshold. <br>
smooth_att_2+fsid.py: Code for Smooth Attention module implementation for FSID Dataset at 2 threshold. <br>
smooth_att_2+fssd.py: Code for Smooth Attention module implementation for FSSD Dataset at 2 threshold. <br>
smooth_att_2+kvasir.py: Code for Smooth Attention module implementation for Kvasir-Instruments Dataset at 2 threshold. <br>
smooth_att_2+lsdsc.py: Code for Smooth Attention module implementation for LSDSC Dataset at 2 threshold. <br>
<br>
viz_smooth_att_0_4+fssd.py: Code for example results vizualisation for FSSD Dataset at 0.4 threshold. <br>
viz_smooth_att_2_0+fssd.py: Code for example results vizualisation for FSSD Dataset at 2 threshold. <br>

README.md: This file, containing an overview of the repository. <br>
LICENSE: Apache 2.0 License. <br>
