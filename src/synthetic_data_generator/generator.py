import logging
import random
import numpy as np
from utils import create_weighted_generator, add_random_spacing
from chapters_layout import generate_chapter_layout, format_chapter
from subchapters_layout import format_subchapter
from noise_generators import generate_systemic_noise_layout, format_systemic_noise, generate_random_noise


def generate_synthetic_data(json_data,
                            toc_noise,
                            subchapter_random_noise=.2,
                            chapter_random_noise=.3,
                            chapter_systemic_noise=.2,
                            add_subchapter=.3
                            ):

    # randomness variables
    first_page_numbers = [1, 2, 3, 4, 5]
    first_page_weights = [6, 3, 3, 1, 1]  # 3 and 4 are 5x more likely
    page_range_numbers = np.arange(5, 60)  
    page_range_weights = np.where((page_range_numbers >= 15) & (page_range_numbers <= 35), 3, 1)

    # output variables
    output_data = []

    for book in json_data:
        
        # set new book name for each book
        logging.debug("\nNew book:")
        book_name = book["name"]
        number_of_chapters = book["chapters_counts"]
        current_chapter = {}
        prompt = ""

        # set book layout variables
        book_layout = generate_chapter_layout()

        # set systemic noise layout if needed
        add_systemic_noise = random.choices([0, 1], weights=[1-chapter_systemic_noise, chapter_systemic_noise], k=1)[0]
        if add_systemic_noise:
            noise_layout = generate_systemic_noise_layout()
        
        # define chapters numbers to use
        number_of_chapters_subset = create_weighted_generator(number_of_chapters, max_ceiling=None, start=5, weight_range=(7, 11), weight_multiplier=3)
        chapters_ids = np.random.choice(range(1,number_of_chapters+1),
                                        size=number_of_chapters_subset,
                                        replace=False)
        
        # define wheter to add subchapters
        add_subchapters = random.choices([0, 1], weights=[1-add_subchapter, add_subchapter], k=1)[0]
        if add_subchapters:
            use_numbers = random.choices([0,1], weights=[.85,.15], k=1)[0]
            add_page = random.choices([0,1], weights=[.75,.25], k=1)[0]

        # initialise labe
        book_label = '```json\n[\n'

        for idx,chapter_id in enumerate(chapters_ids):
            for chapter in book['chapters']:
                if chapter["number"] == chapter_id:

                    # get chapter information
                    chapter_title = chapter["title"]
                    chapter_number = idx + 1
                    number_of_subchapter = chapter["subchapter_count"]

                    # get chapters pages
                    if not bool(current_chapter):
                        logging.debug("new chapter")
                        start_page = int(random.choices(first_page_numbers, weights=first_page_weights, k=1)[0])
                        end_page = int(start_page + random.choices(page_range_numbers, weights=page_range_weights, k=1)[0])
                    else:
                        logging.debug("continue chapter")
                        start_page = current_chapter["end_page"] + 1
                        end_page = int(start_page + random.choices(page_range_numbers, weights=page_range_weights, k=1)[0])

                    # add label
                    current_chapter = {
                        "chapter_number": chapter_number,
                        "chapter_title": chapter_title,
                        "start_page": start_page,
                        "end_page": end_page
                    }
                    book_label += format_labels(chapter_number, chapter_title, start_page, end_page)
                    logging.debug(f"{current_chapter}")

                    # define chapter layout
                    formatted_chapter = format_chapter(
                        book_layout,
                        chapter_title,
                        chapter_number,
                        start_page
                    )

                    # add chapter to prompt
                    prompt += f"{formatted_chapter}\n"
                        
                    # set noise variables
                    if add_systemic_noise:
                        prompt += format_systemic_noise(noise_layout, start_page, end_page, toc_noise)

                    # add random noise
                    add_random_noise = random.choices([0, 1], weights=[1-chapter_random_noise, chapter_random_noise], k=1)[0]
                    if add_random_noise:
                        prompt += generate_random_noise('random', toc_noise) + "\n"
                    
                    # add subchapters
                    if number_of_subchapter and add_subchapters: 
                        number_of_subchapters_to_use = create_weighted_generator(number_of_subchapter, max_ceiling=9, start=2, weight_range=(3, 5), weight_multiplier=3)
                        number_of_subchapters_to_use = random.randint(1, number_of_subchapter)
                        actual_chapter_number = chapter["number"]
                        
                        # define subchapters params
                        counter_ids = chapter_number + .1
                        page_range = end_page - start_page
                        
                        # adjust number of subchapters based on page range
                        if page_range <= number_of_subchapters_to_use:
                            number_of_subchapters_to_use = page_range - 2
                        
                        # NOW generate subchapters_ids with the final count
                        all_subchapters_ids = [f"{actual_chapter_number}.{i}" for i in range(1, number_of_subchapter + 1)]
                        subchapters_ids = np.random.choice(all_subchapters_ids,
                                                        size=number_of_subchapters_to_use,
                                                        replace=False)
                        
                        # generate pages array (now same size as subchapters_ids)
                        subchapters_pages = np.sort(np.random.choice(range(start_page, end_page), 
                                                                size=number_of_subchapters_to_use, 
                                                                replace=False))

                        # loop trough subchapters
                        for idx_sub, subchapter_id in enumerate(subchapters_ids):
                            for subchapter in chapter['subchapters']:
                                if subchapter["number"] == subchapter_id:
                                    prompt += format_subchapter(subchapter["title"], 
                                                                counter_ids, 
                                                                subchapters_pages[idx_sub], 
                                                                use_numbers, 
                                                                add_page)
                                    counter_ids = round(counter_ids + 0.1, 1)     
                                    add_random_noise_to_subchapters = random.choices([0, 1], weights=[1-subchapter_random_noise, subchapter_random_noise], k=1)[0]
                                    if add_random_noise_to_subchapters:
                                        prompt += generate_random_noise('subchapters', toc_noise) + "\n"           

                    logging.debug(f"Chapter layout: {formatted_chapter}")
        
        # finish label format
        book_label = book_label[:-2] +'\n]\n```'
        output_data.append((prompt, book_label))
        logging.info(f"{prompt}")

    return output_data