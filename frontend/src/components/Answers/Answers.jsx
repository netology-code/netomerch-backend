/* eslint-disable no-param-reassign */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/click-events-have-key-events */
import React, { useState } from 'react';
import Accordion from './Accordion/Accordion';
import style from './answers.module.css';
import Title from '../ui/Title';

const mockData = [
  {
    id: 1,
    question: 'Вопрос про Нетологию #1 Вопрос про Нетологию #1 Вопрос про Нетологию #1 Вопрос про Нетологию #1 Вопрос про Нетологию #1Вопрос про Нетологию #1 ',
    answer: 'Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum',
    isOpen: false,
  },
  {
    id: 2,
    question: 'Вопрос про Нетологию #2',
    answer: 'Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum',
    isOpen: false,
  },
  {
    id: 3,
    question: 'Вопрос про Нетологию #3',
    answer: 'Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum',
    isOpen: false,
  },
  {
    id: 4,
    question: 'Вопрос про Нетологию #4',
    answer: 'Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum',
    isOpen: false,
  },
];

const Answers = () => {
  const [content, setContent] = useState(mockData);
  const handleClick = (id) => {
    setContent(content.map((cont) => {
      if (id === cont.id) {
        cont.isOpen = !cont.isOpen;
      } else {
        cont.isOpen = false;
      }
      return cont;
    }));
  };

  return (
    <section className={style.answers}>
      <div className="container">
        <header>
          <Title text="Раздел с ответами на часто встречающиеся вопросы" sqSize="25" />
        </header>

        <div className={style.accordion}>
          { content.map((item) => (
            <Accordion
              key={item.id}
              id={item.id}
              title={item.question}
              content={item.answer}
              isOpen={item.isOpen}
              onClick={handleClick}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Answers;
