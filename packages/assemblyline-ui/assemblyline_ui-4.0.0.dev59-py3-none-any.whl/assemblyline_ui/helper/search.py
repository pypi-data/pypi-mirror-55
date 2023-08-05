from assemblyline_ui.config import STORAGE

BUCKET_MAP = {
    'alert': STORAGE.alert,
    'file': STORAGE.file,
    'heuristic': STORAGE.heuristic,
    'result': STORAGE.result,
    'signature': STORAGE.signature,
    'submission': STORAGE.submission,
    'workflow': STORAGE.workflow
}


def list_all_fields():
    return {k: BUCKET_MAP[k].fields() for k in BUCKET_MAP.keys()}
