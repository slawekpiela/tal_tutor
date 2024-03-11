# correct version
def create_records_from_triplets(triplets):
  records = {
    'records': [
      {'fields': {
        'keyword': word,
        'transcription': transcription,
        'translation': translation + '<<',
        'study_status': '---',
        'translation_extended': '',
        'user': 'slawek',
        'no_of_tries': 0,
        'group': 'general'
      }} for word, transcription, translation in triplets
    ]
  }
  return records