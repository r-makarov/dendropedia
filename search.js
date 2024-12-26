
async function fetchPages() {
    try {
        const response = await fetch('pages.json');
        return await response.json();
    } catch (error) {
        console.error("Error fetching pages data:", error);
        return { pages: [] }; 
    }
}


function cleanTitle(rawTitle) {    
    return rawTitle.replace(/^\d+_/, '').replace(/_/g, ' ');
}


function findRelevantPage(query, pages) {
    for (const page of pages) {
        const cleanPageTitle = cleanTitle(page.title); 

        if (cleanPageTitle.toLowerCase().includes(query.toLowerCase()) && page.url) {
            console.log("Match found:", cleanPageTitle, "=>", page.url);
            return page.url;
        }
        
        if (page.children) {
            const childResult = findRelevantPage(query, page.children);
            if (childResult) {
                return childResult; 
            }
        }
    }
    return null; 
}


document.addEventListener("DOMContentLoaded", async () => {
    const searchForm = document.querySelector('#searchForm');
    const searchInput = document.querySelector('#search');
    const pagesData = await fetchPages();

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault(); 

        const query = searchInput.value.trim();
        if (!query) {
            alert("Please enter a search term.");
            return;
        }

        const relevantPageUrl = findRelevantPage(query, pagesData.pages);
        if (relevantPageUrl) {
            window.location.href = relevantPageUrl; 
        } else {
            alert("No relevant pages found!");
        }
    });
});
