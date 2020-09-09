const Get = require('request-promise');
const cheerio = require('cheerio');
const PDFDocument = require('pdfkit');
const download = require('image-downloader');
fs = require('fs');

function Manga(name) {
  const pag = [];
  let base_url = 'https://mangayabu.com/?s='
  var name = name.split(' ').join('+');
  let url = base_url + name

  Get(url)
  .then(function(html){
    let $ = cheerio.load(html)
    var getmanga = $('a')[8].attribs.href

  Get(getmanga)
  .then(function(html){
    let $ = cheerio.load(html);
    var getcapmanga = $('a')[164].attribs.href
  Get(getcapmanga)
  .then(function(html){
    let $ = cheerio.load(html)
    $('img').each(function(i,elem){
      pag[i] = $(this).attr().src;
    });
    pag.join(', ');
    var i;
    for (let i = 0; i < pag.length; i++) {
      const options = {
        url: pag[i],
        dest: '/home/gabriel/Documentos/GIT/js-api-manga/claymore_'+i ,
        extractFilename: false
      }
      download.image(options)
      .then(({ filename = 'claymore_'+i, image }) => {
      console.log('Saved to',filename)  // Saved to /path/to/dest/image.jpg
      })
    }});
  });
  });
};
// Manga('claymore')

function Generate() {
  const doc = new PDFDocument;
  doc.pipe(fs.createWriteStream('caymore_1.pdf'));
  for (let i = 0; i < 70; i++) {
    doc.image('/home/gabriel/Documentos/GIT/js-api-manga/claymore_'+i , {
      fit: [500, 700],
      align: 'center',
      valign: 'center'
   });
   doc.addPage()
  }  
  doc.end();
}

Generate()