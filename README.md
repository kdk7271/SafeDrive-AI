# 졸음 운전 및 전방주시 태만 방지 시스템

## 프로젝트 개요

고속도로 교통사고의 주요 원인 중 하나는 졸음운전과 전방 주시 태만이며, 이는 운전자의 의지와 관계없이 발생하여 스스로 감지하고 대처하기 어렵습니다. 이러한 사고는 치명적인 결과를 초래할 가능성이 높으며, 기존의 방지 방법으로는 졸음쉼터 이용이나 신체 부착형 방지 장치 등이 있지만, 후자의 경우 불편함과 지속적인 사용의 어려움이 존재합니다.

이에 따라 본 프로젝트에서는 사용자의 신체에 부착하지 않고도 효과적으로 졸음운전 및 전방 주시 태만을 감지하고 경고할 수 있는 시스템을 개발하고자 합니다. CNN 기반의 영상 처리 기술을 활용하여 운전자의 상태를 실시간으로 분석하고, 졸음 또는 주의 분산이 감지될 경우 즉각적인 경고를 제공함으로써 교통사고를 예방하는 것을 목표로 합니다.

## 사용 데이터

[Closed Eye Databases](https://parnec.nuaa.edu.cn/_upload/tpl/02/db/731/template731/pages/xtan/ClosedEyeDatabases.html)

![Image](https://github.com/user-attachments/assets/7185ba5e-b980-490f-aa53-3f5d35ff4341)

* 눈을 감고 있는 이미지, 눈을 뜨고 있는 이미지

![Image](https://github.com/user-attachments/assets/65bc753e-e35b-4a98-a42b-56a73f93d856)

* 데이터 분포

![Image](https://github.com/user-attachments/assets/aec848b7-52f1-48c4-8d84-a4a92b2cdb07)


* 데이터 증강(Data Augmentation)
```
  1. Rescaling(정규화): 흑백 이미지의 각각의 픽셀 값을 255로 나누어 0에서 1 사이의 값으로 변환하였다.
  2. Rotation(회전): 이미지를 10도 회전시켜 다양한 각도에서도 인식할 수 있도록 하였다.
  3. Width Shift(수평 이동): 이미지를 수평 방향으로 0.2 비율만큼 이동시켜, 위치 변화에 대한 모델의 일반화 성능을 높였다.
  4. Height Shift(수직 이동): 이미지를 수직 방향으로 0.2 비율만큼 이동시켜, 다양한 위치에서도 모델이 학습할 수 있도록 하였다.
  5. Shear(기울기 변환): 이미지를 0.2 비율만큼 기울여 다양한 형태의 변형에도 대응할 수 있도록 하였다.
```

## 모델링

![Image](https://github.com/user-attachments/assets/df4700c3-c5e4-4470-92ff-fd12ecc00372)

```
1. CNN 기반 이진 분류 모델로, 입력 이미지(26x34)를 Conv2D와 MaxPooling을 거쳐 특징을 추출한 후, Dense 레이어로 분류하였다.
2. 모델링 구성: 3개의 Conv2D + MaxPooling, Flatten 후 2개의 Dense 레이어(ReLU 활성화, 최종 출력 1개) 를 사용하였다.
3. 하이퍼파라미터: Adam Optimizer, Binary Cross Entropy, 50 Epochs, Batch Size 32 을 사용하였다.
```

## 모델링 결과

![Image](https://github.com/user-attachments/assets/75251593-ce00-4c26-985b-7fb1e6fcf606)

![Image](https://github.com/user-attachments/assets/4acd5d7a-0c0a-46eb-8e06-a79f884fdeaf)

* 테스트 결과 모든 상황에 눈의 개폐 여부를 정확하게 분류하였다.

![Image](https://github.com/user-attachments/assets/89ad742d-c3ad-4948-935c-e7f240b51df1) ![Image](https://github.com/user-attachments/assets/cd80297e-dcf1-4590-90c6-c2c1c968119e)

* 실제 상황에서도 눈의 개폐 여부를 적절히 분류하였다.


## 시스템 구축


* 졸음운전 상황(1) 경고

[https://github.com/user-attachments/assets/4bb8cba7-b09c-4708-a11f-4c95d7af8a90 ](https://github.com/user-attachments/assets/f22aacb4-a8c5-4bf7-bb3c-3d2c0b0f2f36)

* 졸음운전 상황(2) 경고
  
[https://github.com/user-attachments/assets/f22aacb4-a8c5-4bf7-bb3c-3d2c0b0f2f36](https://github.com/user-attachments/assets/ba0c4aab-6f70-49e5-86b7-56c03811b716)

* 전방 주시 태만 경고
  
[https://github.com/user-attachments/assets/cb82f09f-7e9e-4ebd-9870-045f94909db1](https://github.com/user-attachments/assets/cb82f09f-7e9e-4ebd-9870-045f94909db1)

![Image](https://github.com/user-attachments/assets/7eaeebcd-5d1b-4ec9-b2ff-18e3318d9257)

* 3회 이상 연속 경고시 응급 상황으로 판단하여 긴급 문자를 자동으로 발송합니다.

## 트러블 슈팅


