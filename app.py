from flask import *
import script.search as search
import script.chunk as chunk
import script.get_res_tags as gt
from midi_proc import proc_midi
from script.midi_to_audio import midi2audio
import time
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('Index.html')
    else:
        content = []
        res = search.search_1(request)
        tags = gt.get_tags(res)
        musics=[]
        count=len(res)
        for i in range(count):
            # Process the tags and create the musics
            temp=proc_midi(tags[i],res[i]['content'],i)
            filename = time.time()
            addr=midi2audio(temp,'./static/WAV/{}.wav'.format(filename))
            musics.append(addr)
            time.sleep(0.1)
            print("Processed: ",addr)
            # Chunk the poems.
            if res[i]['content'][5] == '，':
                content.append(list(chunk.chunks(res[i]['content'], 6)))
            else:
                content.append(list(chunk.chunks(res[i]['content'], 8)))
        return render_template(
            'Search.html',
            count=count,
            result=res,
            content=content,
            musics=musics)


if __name__ == '__main__':
    app.run()
