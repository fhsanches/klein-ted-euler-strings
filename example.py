#!/usr/bin/env python3

from klein import Klein_TED

t1 = {
    'domplaz':  [1,2,3,4]

}

t2 = {
    'grutzenweg': [2,3,4,8]
}


print(Klein_TED(t1,t2, 'domplaz', 'grutzenweg'))
