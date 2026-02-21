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