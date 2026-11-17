/**
 * Fig Leaf review ticks: collects every pick into this Google Sheet.
 * Paste this whole file into Extensions > Apps Script of the sheet, then
 * deploy it as a web app (see google-sheet-setup.md next to this file).
 *
 * One row per reviewer, page and section. Changing a pick updates its row;
 * taking a pick back (no tick and no comment) clears the verdict on its row.
 */
var SHEET_NAME = 'Picks';
var HEADERS = ['Reviewer', 'Concept', 'Page', 'Section', 'Verdict', 'Comment', 'Link', 'Updated', 'Key'];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var data = JSON.parse(e.postData.contents);
    var rows = data.rows || [];
    var sheet = getSheet_();
    var keys = sheet.getLastRow() > 1
      ? sheet.getRange(2, HEADERS.length, sheet.getLastRow() - 1, 1).getValues().map(function (r) { return r[0]; })
      : [];
    rows.forEach(function (r) {
      var key = (r.reviewerId || '') + '|' + (r.key || '');
      var values = [
        r.reviewer || '(no name) ' + (r.reviewerId || ''),
        r.concept || '', r.page || '', r.section || '',
        r.verdict || '', r.comment || '', r.url || '',
        r.at ? new Date(r.at) : new Date(), key
      ];
      var at = keys.indexOf(key);
      if (at > -1) {
        sheet.getRange(at + 2, 1, 1, values.length).setValues([values]);
      } else {
        sheet.appendRow(values);
        keys.push(key);
      }
    });
    return ContentService.createTextOutput(JSON.stringify({ ok: true, saved: rows.length }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// Opening the web app URL in a browser just confirms it is live.
function doGet() {
  return ContentService.createTextOutput('Fig Leaf review collector is running.');
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.hideColumns(HEADERS.length);
  }
  return sheet;
}
