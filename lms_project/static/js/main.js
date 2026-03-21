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