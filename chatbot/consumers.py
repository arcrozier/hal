import json
import logging
import re
from typing import Final

from channels.generic.websocket import AsyncWebsocketConsumer
from tensorflow.python.framework.errors_impl import InvalidArgumentError


class MessageConsumer(AsyncWebsocketConsumer):

    placeholder: Final = "I don't understand"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.on = False
        self.conversation = ''
        self.pending = 0

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # shut down model
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        category = text_data_json['type']

        if category == "status":
            if message == "on":
                # imports necessary dependencies - won't need to be imported later
                import tensorflow.compat.v1 as tf
                from .gpt2.src import model, sample, encoder
                logging.getLogger(__name__).info('Dependencies loaded')
                self.on = True
                await self.send(json.dumps({  # tells webpage that the model is ready
                    'type': 'status',
                    'message': 'on'
                }))
            elif message == "off":
                self.on = False
        if category == "message" and self.on:
            # may want to store message history and pass it to the model rather than just the latest message
            self.conversation = '\n'.join([self.conversation, message])
            self.pending += 1
            sample = self.interact_model(self.conversation)
            find_eot = re.match(r'.+?(?=<\|endoftext\|>|$)', sample, re.DOTALL)
            find_sentence = re.match(r'(?:.+?[.!?][ \n]){2}', sample, re.DOTALL | re.MULTILINE)

            print(find_eot, find_sentence)

            if find_eot is not None and find_sentence is not None:
                reply = find_eot if len(find_eot.group(0)) < len(find_sentence.group(0)) else find_sentence
            else:
                reply = find_eot if find_eot is not None else find_sentence

            if reply is None:
                reply = self.placeholder
            else:
                reply = reply.group(0)

            self.conversation = '\n'.join([self.conversation, reply])

            await self.send(json.dumps({
                'type': 'reply',
                'message': reply,
            }))
            self.pending -= 1
        print(self.pending)

    def make_response(self, prompt: str):
        # this is where hyper parameter tuning would go
        self.interact_model(prompt, length=1, top_k=40, top_p=0.9)

    @staticmethod
    def interact_model(
            prompt: str,
            model_name: str = '117M',
            seed: int = None,
            length: int = None,
            temperature: float = 1,
            top_k: int = 0,
            top_p: float = 0.0
    ):
        """
        Interactively run the model

        :prompt : String, the prompt for the model to generate with
        :model_name=117M : String, which model to use
        :seed=None : Integer seed for random number generators, fix seed to reproduce
         results
        :length=None : Number of tokens in generated text, if None (default), is
         determined by model hyperparameters
        :temperature=1 : Float value controlling randomness in boltzmann
         distribution. Lower temperature results in less random completions. As the
         temperature approaches zero, the model will become deterministic and
         repetitive. Higher temperature results in more random completions.
        :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
         considered for each step (token), resulting in deterministic completions,
         while 40 means 40 words are considered at each step. 0 (default) is a
         special setting meaning no restrictions. 40 generally is a good value.
        :top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
         overriding top_k if set to a value > 0. A good setting is 0.9.
        """
        import numpy as np
        import os
        import tensorflow.compat.v1 as tf
        from .gpt2.src import model, sample, encoder

        batch_size = 1

        enc = encoder.get_encoder(model_name)
        hparams = model.default_hparams()
        with open(os.path.join(os.path.dirname(__file__), 'gpt2', 'src', 'models', model_name, 'hparams.json')) as f:
            dict2 = json.load(f)
            for key, value in hparams.items():
                hparams[key] = dict2[key]

        if length is None:
            length = hparams['n_ctx'] // 2
        elif length > hparams['n_ctx']:
            raise ValueError("Can't get samples longer than window size: %s" % hparams['n_ctx'])

        with tf.Session(graph=tf.Graph()) as sess:
            context = tf.placeholder(tf.int32, [batch_size, None])
            np.random.seed(seed)
            tf.set_random_seed(seed)
            output = sample.sample_sequence(
                hparams=hparams, length=length,
                context=context,
                batch_size=batch_size,
                temperature=temperature, top_k=top_k, top_p=top_p
            )

            saver = tf.train.Saver()
            ckpt = tf.train.latest_checkpoint(os.path.join(os.path.dirname(__file__), 'gpt2', 'src', 'models', model_name))
            saver.restore(sess, ckpt)

            context_tokens = enc.encode(prompt)

            for _ in range(0, 5):
                try:
                    out = sess.run(output, feed_dict={
                        context: [context_tokens]
                    })[:, len(context_tokens):]
                    text = enc.decode(out[0])
                    print("=" * 40 + " SAMPLE " + "=" * 40)
                    print(text)
                    return text
                except InvalidArgumentError as e:
                    print(str(e))
