const app = document.getElementById('app');
const projectList = document.querySelector('.project-list');
const heroText = document.querySelector('.hero-text');
const projectDetail = document.querySelector('.project-detail');

// Intro Text
const INTRO_COPY = "Selected Works. 2014—2026. Defining digital aesthetics for the modern era.";

// Footer Content
const FOOTER_HTML = `
    <footer class="site-footer">
        <div class="footer-column">
            <h3 class="footer-heading">About</h3>
            <p class="footer-text">
                Digital Product Designer crafting purposeful interfaces and identities. 
                Formerly at Rolls-Royce, Samsung, and Volvo. 
                Obsessed with typography and the space between things.
            </p>
        </div>
        <div class="footer-column">
            <h3 class="footer-heading">Contact</h3>
            <a href="mailto:hello@mikkopi.com" class="footer-link">hello@mikkopi.com</a>
            <a href="#" class="footer-link">LinkedIn</a>
            <a href="#" class="footer-link">Instagram</a>
        </div>
    </footer>
`;

async function init() {
    // Inject Footer
    if (app) {
        app.insertAdjacentHTML('beforeend', FOOTER_HTML);
    }

    // Set intro
    if (heroText) heroText.textContent = INTRO_COPY;

    try {
        const response = await fetch('data.json');
        const projects = await response.json();

        // Router logic
        const path = window.location.pathname;
        const searchParams = new URLSearchParams(window.location.search);
        const slug = searchParams.get('slug');

        if (slug && (path.includes('project.html') || document.getElementById('project-detail-view'))) {
            renderProjectDetail(projects, slug);
        } else if (projectList) {
            renderProjects(projects);
        }
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

function renderProjects(projects) {
    if (!projectList) return;

    const html = projects.map((project, index) => {
        if (project.slug === 'home') return '';

        const coverImage = project.images.length > 0 ? project.images[0] : '';

        // Check if collection
        const isCollection = project.slug.includes('experiments') || project.slug.includes('transportation');

        return `
            <article class="project-card" data-slug="${project.slug}" data-collection="${isCollection}">
                <a href="project.html?slug=${project.slug}" class="project-link">
                    <div class="project-image-container">
                        ${coverImage ? `<img src="${coverImage}" alt="${project.title}" loading="lazy">` : '<div class="no-image"></div>'}
                    </div>
                    <div class="project-info">
                        <h2 class="project-title">${project.title.replace('—', '').replace('&mdash;', '')}</h2>
                        <p class="project-description">${project.description}</p>
                    </div>
                </a>
            </article>
        `;
    }).join('');

    projectList.innerHTML = html;
}

function renderProjectDetail(projects, slug) {
    const project = projects.find(p => p.slug === slug);
    const container = document.getElementById('project-detail-view');

    if (!project || !container) {
        if (container) container.innerHTML = '<h1>Project not found</h1>';
        return;
    }

    document.title = `${project.title} - Mikkopi`;

    const imagesHtml = project.images.map(img => `
        <figure class="detail-image-block">
            <img src="${img}" alt="${project.title} image" loading="lazy">
        </figure>
    `).join('');

    const html = `
        <header class="project-header">
            <h1 class="detail-title">${project.title.replace('—', '').replace('&mdash;', '')}</h1>
            <div class="detail-meta">
                <p class="detail-description">${project.description}</p>
            </div>
        </header>
        
        <div class="project-content">
            ${imagesHtml}
        </div>
        
        <div class="project-footer">
            <a href="index.html" class="back-link">← Index</a>
        </div>
    `;

    container.innerHTML = html;
}

init();
