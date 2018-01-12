from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np
import translate as tr

def graph_reco(path):
    model = MobileNet(weights='imagenet')

    img_path = path
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    predict_list = decode_predictions(preds, top=3)[0]
    to_trans = []
    for i in predict_list:
        to_trans.append(' '.join(str(i[1]).split('_')))
    translator = tr.Youdao_translate()
    res = []
    for i in to_trans:
        res.append(translator.get_translation(i))

    return res

