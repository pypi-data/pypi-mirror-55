import kachery as ka
import os

ka.set_config(
    url='http://132.249.245.245:24342',
    channel='public',
    password='public',
    download=True
)

X = ka.load_object('sha1://04a29bf145a2833533527262f5f30104bcc53679/analysis.json')
basedir = 'spikeforest_data'
if not os.path.exists(basedir):
    os.mkdir(basedir)

studysets_to_include = ['PAIRED_KAMPFF']
studies_to_include = ['paired_kampff']  
fnames = ['geom.csv', 'params.json', 'raw.mda', 'firings_true.mda']
# fnames = ['geom.csv', 'params.json']  
for studyset in X['StudySets']:
    studyset_name = studyset['name']
    if studyset_name in studysets_to_include:
        print('STUDYSET: {}'.format(studyset['name']))
        studysetdir_local = os.path.join(basedir, studyset_name)
        if not os.path.exists(studysetdir_local):
            os.mkdir(studysetdir_local)
        for study in studyset['studies']:
            study_name = study['name']
            print('STUDY: {}'.format(study_name))
            if study_name in studies_to_include:
                studydir_local = os.path.join(studysetdir_local, study_name)
                if not os.path.exists(studydir_local):
                    os.mkdir(studydir_local)
                for recording in study['recordings']:
                    recname = recording['name']
                    print('RECORDING: {}'.format(recname))
                    recdir = recording['directory']
                    recdir_local = os.path.join(studydir_local, recname)
                    if not os.path.exists(recdir_local):
                        os.mkdir(recdir_local)
                    for fname in fnames:
                        ka.load_file(recdir + '/' + fname, os.path.join(recdir_local, fname))
