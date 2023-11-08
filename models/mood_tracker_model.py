from .entities.mood_record  import MoodRecord


class MoodTrackerModel:
    @classmethod
    def add_record(cls, db, user_id, mood_record):
        """Creates a new record of the user """
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO mood_tracker (user_id, date, emotions, well_being_level)
               VALUES (%s, %s, %s, %s)"""

            # Preparing Strings to be compatible with MySQL
            emotions_string = '[' + ', '.join(map(str, mood_record.emotions)) + ']'
            formatted_datetime = mood_record.date.strftime('%Y-%m-%d %H:%M:%S')

            values = (user_id, formatted_datetime, emotions_string, mood_record.well_being_level)

            cursor.execute(sql, values)

            # commit changes
            db.connection.commit()
            cursor.close()

        except Exception as ex:

            raise Exception(ex)

    @classmethod
    def retrieve_mood_records(cls, db, user_id):
        """Retrieves all the mood_record"""
        records = []
        try:
            cursor = db.connection.cursor()
            sql = """SELECT  date, emotions, well_being_level FROM mood_tracker
                    WHERE user_id = {}""".format(user_id)
            cursor.execute(sql)

            # retrieve all records
            result = cursor.fetchall()
            for row in result:
                # Reformat string of emotions from [sad, gief, happiness] to ['sad', 'gief', 'happiness']
                emotions_new_format = row[1].replace('[', "['").replace(', ', "', '").replace(']', "']")
                record = MoodRecord(row[0], emotions_new_format, row[2])
                records.append(record)
            cursor.close()
            return records
        except Exception as ex:
            raise Exception(ex)