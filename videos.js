/* ================= EDIT YOUR VIDEOS HERE =================
   This one file feeds BOTH pages: index.html and work.html.
   One line = one video. Copy a line to add a video, delete a line to remove one.
   title : the name shown on the card
   kind  : the category shown under the carousel / under the film (e.g. 'Brand ad')
   dur   : the length shown on the card, as 'minutes:seconds'
   role  : (short-form only) what you did on it, shown under the carousel
   src   : the video link, in quotes. Either a file in the same folder ('videos/aurora.mp4')
           or a direct .mp4 link from your video host. Leave '' to show the colored placeholder.
   poster: (optional) thumbnail picture shown before the video plays, e.g. 'thumbs/aurora.jpg' or a full
           https link. Leave '' and the site shows the first frame of the video instead.
   hue   : placeholder color (0-360), only used while src and poster are empty
   sample: no longer used, safe to ignore
   Keep the commas between lines and the quotes around text.
   ========================================================== */
window.SHORTS = [
  { title: 'Beauty Event Jeddah',          kind: 'Event recap',    dur: '1:00', hue: 190, role: 'Edit · sound design · color',         poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/mayam.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Mayam%20Reel%201.mp4', sample: true },
  { title: 'Talking Head Content',         kind: 'Marketing tips', dur: '0:42', hue: 24,  role: 'Edit · motion tracking · captions',   poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/ugc%202.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Bishoy%20Media%20Buyer%2011%20Fhd.mp4', sample: true },
  { title: 'Talking Head Doctor',          kind: 'Medical info',   dur: '0:38', hue: 340, role: 'Edit · color · motion',               poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/ugc%203%20doctor.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Fc%20Clinic%20Reel%204%20PORTFOLIO.mp4', sample: true },
  { title: 'Jewelry Store',                kind: 'Store ad',       dur: '0:16', hue: 210, role: 'Edit · b-roll · color',               poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/jewelery%20store.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Louis%20Jewl%20Bag%20PORTFOLIO.mp4', sample: true },
  { title: 'Food Plates Speed Ramps',      kind: 'Restaurant ad',  dur: '0:17', hue: 150, role: 'Edit · sound design · speed ramps',   poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/food%20speed%20ramps.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Lustro%20Ramps%20Reel%20Final%20PORTFOLIO.mp4', sample: true },
  { title: 'Talking Head Business',        kind: 'Business ad',    dur: '0:27', hue: 285, role: 'Edit · b-roll · color',               poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/ugc%201.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Arabic%20Reel%20Final%20PORTFOLIO.mp4', sample: true },
  { title: 'Cars Business Promo',          kind: 'Business ad',    dur: '0:27', hue: 48,  role: 'Edit · hooks · b-roll',               poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/seat.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Seat%20Sharkia%20Edit.mp4', sample: true },
  { title: 'Cards Game Promo',             kind: 'Entertainment',  dur: '1:38', hue: 190, role: 'Edit · stop motion · motion design',  poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/eyad.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Eb3thaloo%202Ool%20Ameeme%20X%20Eyad%20Final%20PORTFOLIO.mp4', sample: true },
  { title: 'Dental Clinic Promo',          kind: 'Business ad',    dur: '0:21', hue: 8,   role: 'Edit · b-roll · color',               poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/clinic.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Lucid%20Dental%20Center%20PORTFOLIO.mp4', sample: true },
  { title: 'Tech Podcast',                 kind: 'Podcast',        dur: '0:44', hue: 120, role: 'Edit · captions · multi-cam',         poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/apple.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/iSupport%20reel%202.mp4', sample: true },
  { title: 'Salon Business Promo',         kind: 'Business ad',    dur: '0:45', hue: 255, role: 'Edit · beat-synced cuts · color',     poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/salon.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Triv%20X%20Zizo%20PORTFOLIO.mp4', sample: true }
];
window.FILMS = [
  { title: 'Marriage Story Short Film',    kind: 'Documentary',   dur: '3:47', hue: 210,  poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/marriage.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Abd%20Elelah%20Short%20Wed%20Film%20Final%20222.mp4', sample: true },  
  { title: 'Udacity Educational Content',  kind: 'Educational',  dur: '3:39',  hue: 24,  poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/udacity.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/udacity%20video%20jave%20web%20dev.mp4', sample: true },
  { title: 'Product Feedback from Clients',    kind: 'Interview',   dur: '2:46', hue: 210, poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/reeq%20elnahl.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/Reeq%20Alnahl%20Final%20With%20Captions%20PORTFOLIO.mp4', sample: true },
  { title: 'Politics News YouTube',             kind: 'News', dur: '7:48',  hue: 300, poster: 'https://pub-be1388614de444c581c12a700d1bf992.r2.dev/politics.jpg', src: 'https://pub-34bb1b1a86f74630a4091e4c415dc302.r2.dev/street%20politics%20video.mp4', sample: true }
];
