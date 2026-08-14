from pathlib import Path
import sqlite3

# working directories
working_dir = Path(__file__).parent.absolute()
db = working_dir.parent / 'db' / 'main.sqlite'

# connect to database
connection = sqlite3.connect(db)
cursor = connection.cursor()

try:

    # reset completeness flags
    cursor.execute("UPDATE boards SET is_complete = 0;")

    # check against full criteria (images, species, grade, velocity, impurities all exist for given board id)
    update_query = """
                   UPDATE boards
                   SET is_complete = 1
                   WHERE
                       
                       (front_path IS NOT NULL OR left_path IS NOT NULL OR back_path IS NOT NULL OR \
                        right_path IS NOT NULL)
                       
                     AND (species_name IS NOT NULL AND UPPER(species_name) != 'N/A')

                     AND (grade_name IS NOT NULL AND UPPER(grade_name) != 'N/A')

                     AND board_id IN (SELECT m.board_id \
                                      FROM moe m \
                                               INNER JOIN impurities i ON m.board_id = i.board_id \
                                      WHERE m.velocity > 0 \
                                        AND (i.nails > 0 OR i.staples > 0 OR i.connected_boards > 0 OR i.screws > 0 OR \
                                             i.misc_fasteners > 0)); \
                   """

    cursor.execute(update_query)
    connection.commit()

    cursor.execute("SELECT board_id, species_name, grade_name FROM boards WHERE is_complete = 1;")
    complete_boards = cursor.fetchall()

    print(f"\n{len(complete_boards)} fully complete boards.")

finally:
    # close the connection
    connection.close()