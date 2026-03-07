document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.lesson-link');
  const sections = document.querySelectorAll('.lesson-section');

  function switchLesson(id) {
      sections.forEach(s => s.classList.add('d-none'));
      links.forEach(l => l.classList.remove('active'));
      
      const target = document.getElementById(id);
      const link = document.querySelector(`[href="#${id}"]`);
      if(target) target.classList.remove('d-none');
      if(link) link.classList.add('active');
  }

  links.forEach(link => {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          switchLesson(this.getAttribute('href').substring(1));
          window.scrollTo({top: 0, behavior: 'smooth'});
      });
  });

  if(links.length > 0) switchLesson(links[0].getAttribute('href').substring(1));
});

    function showLesson(lessonId) {
        document.querySelectorAll('.lesson-pane').forEach(el => {
            el.classList.add('d-none');
        });
        
        const target = document.getElementById(lessonId);
        if (target) {
            target.classList.remove('d-none');
            if (window.scrollY > 100) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
        
        document.querySelectorAll('.lesson-item').forEach(el => {
            el.classList.remove('active');
        });
        const activeLink = document.querySelector(`a[href="#${lessonId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const links = document.querySelectorAll('.lesson-item');

        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault(); 
                const lessonId = this.getAttribute('href').substring(1);
                showLesson(lessonId);
            });
        });

        if (links.length > 0) {
            let activeExists = document.querySelector('.lesson-pane:not(.d-none)');
            if (!activeExists) {
                const firstLessonId = links[0].getAttribute('href').substring(1);
                showLesson(firstLessonId);
            }
        }
    });
