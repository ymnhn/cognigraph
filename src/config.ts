export const SITE = {
  // 1. Your actual GitHub Pages URL
  website: "https://ymnhn.github.io/cognigraph/", 
  
  // 2. Your identifier
  author: "CogniGraph Bot",
  profile: "https://github.com/ymnhn",
  
  // 3. Project branding
  desc: "Automated Cognitive Science Research Dashboard & Semantic Curation.",
  title: "CogniGraph",
  
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: false,
  postPerIndex: 10,
  postPerPage: 10,
  scheduledPostMargin: 15 * 60 * 1000,
  showArchives: true,
  showBackButton: true,

  // 4. Disable or update the 'Edit page' button
  editPost: {
    enabled: false, // Set to false since these are bot-generated papers
    text: "Edit page",
    url: "https://github.com/ymnhn/cognigraph/edit/main/",
  },

  dynamicOgImage: true,
  dir: "ltr",
  lang: "en",
  
  // 5. Update to your local timezone
  timezone: "UTC", 
} as const;