document.addEventListener("DOMContentLoaded", function() {
  const questions = [
      {
          question: "Яка мова використовується для стилізації сайтів?",
          answers: ["HTML", "CSS", "JavaScript"],
          correct: "CSS",
          explanation: "CSS (Cascading Style Sheets) відповідає за зовнішній вигляд веб-сторінок."
      },
      {
          question: "Який тег створює абзац у HTML?",
          answers: ["<p>", "<div>", "<span>"],
          correct: "<p>",
          explanation: "Тег <p> використовується для створення абзаців."
      }
  ];

  let currentQuestion = 0;
  let score = 0;
  const questionElement = document.getElementById('question');
  const answersContainer = document.getElementById('answers-container');
  const resultDiv = document.getElementById('result');

  function showQuestion() {
      // Очищаємо попередні відповіді
      answersContainer.innerHTML = '';
      
      // Встановлюємо поточне питання
      questionElement.textContent = questions[currentQuestion].question;
      
      // Додаємо кнопки з відповідями
      questions[currentQuestion].answers.forEach(answer => {
          const button = document.createElement('button');
          button.className = 'btn btn-outline-primary w-100 mb-2';
          button.textContent = answer;
          button.addEventListener('click', () => checkAnswer(answer));
          answersContainer.appendChild(button);
      });
  }

  function checkAnswer(selectedAnswer) {
      const correctAnswer = questions[currentQuestion].correct;
      
      if (selectedAnswer === correctAnswer) {
          score++;
          resultDiv.innerHTML = `
              <div class="alert alert-success">
                  <i class="fas fa-check-circle"></i> Правильно! 
                  ${questions[currentQuestion].explanation}
              </div>
          `;
      } else {
          resultDiv.innerHTML = `
              <div class="alert alert-danger">
                  <i class="fas fa-times-circle"></i> Неправильно. 
                  Правильна відповідь: ${correctAnswer}. 
                  ${questions[currentQuestion].explanation}
              </div>
          `;
      }
      
      // Перехід до наступного питання
      currentQuestion++;
      
      if (currentQuestion < questions.length) {
          setTimeout(showQuestion, 1500);
      } else {
          showResults();
      }
  }

  function showResults() {
      quizContainer.innerHTML = `
          <div class="text-center">
              <h3>Тест завершено!</h3>
              <p class="lead">Ваш результат: ${score} з ${questions.length}</p>
              <button onclick="location.reload()" class="btn btn-primary mt-3">
                  <i class="fas fa-redo"></i> Спробувати ще раз
              </button>
          </div>
      `;
  }

  // Починаємо квіз
  showQuestion();
});