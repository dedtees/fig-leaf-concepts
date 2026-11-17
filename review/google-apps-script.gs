/**
 * Fig Leaf concept review: collects the client's ✓ / ✕ ticks into this sheet.
 *
 * Tabs it keeps up to date (rebuilt after every tick):
 *   Overview      a scoreboard per concept, then a grid of every section (rows)
 *                 by concept (columns): green ✓, red ✕, amber when reviewers
 *                 disagree. Hover a cell with a corner mark to read comments.
 *   By concept    pick a concept from the dropdown in B2 to list its picks.
 *   Comments      every written comment, in concept and page order.
 *   All picks     the raw list: one row per reviewer and section, newest
 *                 change wins (changing a tick updates its row; taking it
 *                 back removes the row). Filters are on.
 *
 * Setup: Extensions > Apps Script, paste this file, Deploy > New deployment >
 * Web app, Execute as Me, Who has access Anyone. Put the /exec URL into
 * ENDPOINT in review/review.js.
 */
var TAB_OVERVIEW = 'Overview';
var TAB_CONCEPT = 'By concept';
var TAB_COMMENTS = 'Comments';
var TAB_PICKS = 'All picks';
var PICK_HEADERS = ['Updated', 'Concept', 'Page', 'Section', 'Verdict', 'Comment', 'Reviewer', 'Link', 'Order', 'Key'];
var PAGE_ORDER = ['Homepage', 'Homeowners', 'Homeowners (scrolling)', 'Homeowners (fade)', 'Quote page', 'Quote form'];

var GREEN = '#d9f2e3', GREEN_INK = '#14532d';
var RED = '#fbdcd8', RED_INK = '#8a1c12';
var AMBER = '#fdf0c8', AMBER_INK = '#7a5200';
var HEAD = '#17402b', HEAD_INK = '#ffffff', BAND = '#eef3f0', LINE = '#c9d3cd';

/* ---- web app ------------------------------------------------------------ */
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(25000);
  try {
    var rows = (JSON.parse(e.postData.contents).rows) || [];
    savePicks_(rows);
    rebuild();
    return json_({ ok: true, saved: rows.length });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}
function doGet() {
  return ContentService.createTextOutput('Fig Leaf review collector is running.');
}
function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/* ---- menu --------------------------------------------------------------- */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Review')
    .addItem('Rebuild the overview', 'rebuild')
    .addToUi();
}

/* ---- the raw list ------------------------------------------------------- */
function picksSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(TAB_PICKS);
  if (!sh) {
    sh = ss.insertSheet(TAB_PICKS);
    sh.getRange(1, 1, 1, PICK_HEADERS.length).setValues([PICK_HEADERS])
      .setFontWeight('bold').setBackground(HEAD).setFontColor(HEAD_INK);
    sh.setFrozenRows(1);
    sh.setColumnWidths(1, 1, 140); sh.setColumnWidths(2, 1, 110); sh.setColumnWidths(3, 1, 120);
    sh.setColumnWidths(4, 1, 230); sh.setColumnWidths(5, 1, 95); sh.setColumnWidths(6, 1, 360);
    sh.setColumnWidths(7, 1, 130); sh.setColumnWidths(8, 1, 220);
    sh.getRange('F:F').setWrap(true);
    sh.getRange('A:A').setNumberFormat('d mmm yyyy, h:mm am/pm');
    sh.hideColumns(9, 2);
  }
  return sh;
}

function savePicks_(rows) {
  var sh = picksSheet_();
  var n = sh.getLastRow() - 1;
  var data = n > 0 ? sh.getRange(2, 1, n, PICK_HEADERS.length).getValues() : [];
  var index = {};
  data.forEach(function (r, i) { index[r[9]] = i; });
  var drop = {};
  rows.forEach(function (r) {
    var key = (r.reviewerId || '') + '|' + (r.key || '');
    if (r.deleted || (!r.verdict && !r.comment)) {
      if (key in index) drop[index[key]] = true;
      return;
    }
    var name = r.reviewer || ('Reviewer ' + String(r.reviewerId || '').slice(0, 4));
    var values = [r.at ? new Date(r.at) : new Date(), text_(r.concept), text_(r.page), text_(r.section),
      r.verdict === 'Like' ? '✓ Like' : r.verdict ? "✕ Don't like" : '', text_(r.comment), text_(name),
      r.url || '', Number(r.order) || 0, key];
    if (key in index) {
      data[index[key]] = values;
      delete drop[index[key]];
    } else {
      index[key] = data.length;
      data.push(values);
    }
    // a name typed later applies to that reviewer's earlier rows too
    if (r.reviewer) data.forEach(function (d) { if (String(d[9]).indexOf((r.reviewerId || '') + '|') === 0) d[6] = r.reviewer; });
  });
  data = data.filter(function (_, i) { return !drop[i]; });
  data.sort(comparePicks_);
  if (n > 0) sh.getRange(2, 1, n, PICK_HEADERS.length).clearContent().clearFormat();
  if (data.length) {
    sh.getRange(2, 1, data.length, PICK_HEADERS.length).setValues(data);
    sh.getRange(2, 1, data.length, 1).setNumberFormat('d mmm yyyy, h:mm am/pm');
    sh.getRange(2, 6, data.length, 1).setWrap(true);
    colourVerdicts_(sh.getRange(2, 5, data.length, 1));
  }
  if (sh.getFilter()) sh.getFilter().remove();
  sh.getRange(1, 1, Math.max(data.length + 1, 2), 8).createFilter();
}

/* ---- ordering ----------------------------------------------------------- */
function conceptRank_(c) {
  var m = /(\d+)/.exec(c);
  if (/^concept/i.test(c) && m) return Number(m[1]);
  return 1000 + String(c).toLowerCase().charCodeAt(String(c).length - 1);
}
function pageRank_(p) {
  var i = PAGE_ORDER.indexOf(p);
  return i < 0 ? 50 : i;
}
function comparePicks_(a, b) {
  return conceptRank_(a[1]) - conceptRank_(b[1]) || pageRank_(a[2]) - pageRank_(b[2]) ||
    a[8] - b[8] || String(a[6]).localeCompare(String(b[6]));
}
function colourVerdicts_(range) {
  var vals = range.getValues();
  range.setBackgrounds(vals.map(function (r) { return [r[0].indexOf('✓') === 0 ? GREEN : r[0] ? RED : null]; }));
  range.setFontColors(vals.map(function (r) { return [r[0].indexOf('✓') === 0 ? GREEN_INK : r[0] ? RED_INK : null]; }));
}

/* ---- the derived tabs ---------------------------------------------------- */
function rebuild() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var picks = picksSheet_();
  var n = picks.getLastRow() - 1;
  var data = n > 0 ? picks.getRange(2, 1, n, PICK_HEADERS.length).getValues() : [];
  buildOverview_(ss, data);
  buildComments_(ss, data);
  buildByConcept_(ss, data);
  // tab order: Overview, By concept, Comments, All picks
  [TAB_OVERVIEW, TAB_CONCEPT, TAB_COMMENTS, TAB_PICKS].forEach(function (name, i) {
    var sh = ss.getSheetByName(name);
    ss.setActiveSheet(sh); ss.moveActiveSheet(i + 1);
  });
  ss.setActiveSheet(ss.getSheetByName(TAB_OVERVIEW));
  var blank = ss.getSheetByName('Sheet1');
  if (blank && blank.getLastRow() === 0 && ss.getSheets().length > 4) ss.deleteSheet(blank);
}

function freshSheet_(ss, name) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clear(); sh.clearNotes();
  sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns()).clearDataValidations();
  if (sh.getFilter()) sh.getFilter().remove();
  sh.setFrozenRows(0); sh.setFrozenColumns(0);
  return sh;
}

function buildOverview_(ss, data) {
  var sh = freshSheet_(ss, TAB_OVERVIEW);
  var concepts = unique_(data.map(function (r) { return r[1]; })).sort(function (a, b) { return conceptRank_(a) - conceptRank_(b); });
  var people = unique_(data.map(function (r) { return r[6]; }));
  var updated = data.reduce(function (m, r) { return r[0] > m ? r[0] : m; }, '');

  sh.getRange('A1').setValue('Fig Leaf concepts: client review').setFontSize(16).setFontWeight('bold').setFontColor(HEAD);
  sh.getRange('A2').setValue(data.length
    ? data.length + ' picks from ' + people.join(', ') + '. Last change ' +
      Utilities.formatDate(updated, ss.getSpreadsheetTimeZone(), 'd MMM yyyy, h:mm a') + '.'
    : 'No picks yet. They appear here as the client ticks sections on the preview site.').setFontColor('#5d6762');

  // Scoreboard
  var row = 4;
  sh.getRange(row, 1, 1, 6).setValues([['Concept', '✓ Likes', "✕ Don't likes", 'Score', 'Comments', 'Best liked sections']])
    .setFontWeight('bold').setBackground(HEAD).setFontColor(HEAD_INK);
  var board = concepts.map(function (c) {
    var mine = data.filter(function (r) { return r[1] === c; });
    var likes = mine.filter(function (r) { return r[4].indexOf('✓') === 0; });
    var dis = mine.filter(function (r) { return r[4].indexOf('✕') === 0; }).length;
    var notes = mine.filter(function (r) { return r[5]; }).length;
    var liked = unique_(likes.map(function (r) { return r[3] + (r[2] !== 'Homepage' ? ' (' + r[2] + ')' : ''); }));
    return [c, likes.length, dis, likes.length - dis, notes, liked.slice(0, 6).join(', ') + (liked.length > 6 ? '…' : '')];
  });
  if (board.length) {
    sh.getRange(row + 1, 1, board.length, 6).setValues(board);
    var scores = sh.getRange(row + 1, 4, board.length, 1);
    sh.setConditionalFormatRules([
      SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThan(0).setBackground(GREEN).setFontColor(GREEN_INK).setRanges([scores]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenNumberLessThan(0).setBackground(RED).setFontColor(RED_INK).setRanges([scores]).build()
    ]);
    sh.getRange(row + 1, 1, board.length, 1).setFontWeight('bold');
    sh.getRange(row + 1, 2, board.length, 4).setHorizontalAlignment('center');
  } else {
    sh.setConditionalFormatRules([]);
  }
  sh.getRange(row, 1, board.length + 1, 6).setBorder(true, true, true, true, true, true, LINE, SpreadsheetApp.BorderStyle.SOLID);
  row += board.length + 3;

  // Grid: sections by concept
  sh.getRange(row - 1, 1).setValue('Every section, by concept').setFontWeight('bold').setFontSize(12).setFontColor(HEAD);
  sh.getRange(row - 1, 3).setValue('✓ like   ✕ don\'t like   amber = mixed   a corner mark means there are comments: hover to read')
    .setFontColor('#5d6762').setFontStyle('italic');
  var sections = {};
  data.forEach(function (r) {
    var k = r[2] + '|' + r[3];
    if (!sections[k]) sections[k] = { page: r[2], section: r[3], order: r[8] };
    sections[k].order = Math.min(sections[k].order, r[8]);
  });
  var list = Object.keys(sections).map(function (k) { return sections[k]; })
    .sort(function (a, b) { return pageRank_(a.page) - pageRank_(b.page) || a.order - b.order; });

  var head = ['Page', 'Section'].concat(concepts);
  sh.getRange(row, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground(HEAD).setFontColor(HEAD_INK)
    .setHorizontalAlignment('center');
  sh.getRange(row, 1, 1, 2).setHorizontalAlignment('left');
  var gridTop = row + 1;
  if (list.length && concepts.length) {
    var values = [], bgs = [], inks = [], notes = [];
    var lastPage = '';
    list.forEach(function (s) {
      var v = [s.page === lastPage ? '' : s.page, s.section], bg = [BAND, null], ink = [HEAD, null], nt = ['', ''];
      lastPage = s.page;
      concepts.forEach(function (c) {
        var cell = data.filter(function (r) { return r[1] === c && r[2] === s.page && r[3] === s.section; });
        var y = cell.filter(function (r) { return r[4].indexOf('✓') === 0; }).length;
        var x = cell.filter(function (r) { return r[4].indexOf('✕') === 0; }).length;
        var text = y && !x ? '✓' + (y > 1 ? ' ' + y : '') : x && !y ? '✕' + (x > 1 ? ' ' + x : '') : y && x ? '✓' + y + '  ✕' + x : cell.length ? '…' : '';
        v.push(text);
        bg.push(y && !x ? GREEN : x && !y ? RED : y && x ? AMBER : null);
        ink.push(y && !x ? GREEN_INK : x && !y ? RED_INK : y && x ? AMBER_INK : '#5d6762');
        nt.push(cell.filter(function (r) { return r[5]; }).map(function (r) {
          return r[6] + (r[4] ? ' (' + r[4].slice(2) + ')' : '') + ': ' + r[5];
        }).join('\n\n'));
      });
      values.push(v); bgs.push(bg); inks.push(ink); notes.push(nt);
    });
    var grid = sh.getRange(gridTop, 1, values.length, head.length);
    grid.setValues(values).setBackgrounds(bgs).setFontColors(inks).setNotes(notes)
      .setBorder(true, true, true, true, true, true, LINE, SpreadsheetApp.BorderStyle.SOLID);
    sh.getRange(gridTop, 3, values.length, concepts.length).setHorizontalAlignment('center').setFontWeight('bold').setFontSize(12);
    sh.getRange(gridTop, 1, values.length, 1).setFontWeight('bold');
    // a heavier line where each page starts
    values.forEach(function (v, i) {
      if (v[0] && i) sh.getRange(gridTop + i, 1, 1, head.length)
        .setBorder(true, null, null, null, null, null, HEAD, SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
    });
  }
  sh.setColumnWidth(1, 120); sh.setColumnWidth(2, 240);
  for (var c = 3; c <= Math.max(head.length, 6); c++) sh.setColumnWidth(c, 105);
  sh.setFrozenRows(0);
  sh.setHiddenGridlines(true);
}

function buildComments_(ss, data) {
  var sh = freshSheet_(ss, TAB_COMMENTS);
  var head = ['Concept', 'Page', 'Section', 'Verdict', 'Comment', 'Reviewer', 'Updated'];
  sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground(HEAD).setFontColor(HEAD_INK);
  sh.setFrozenRows(1);
  var rows = data.filter(function (r) { return r[5]; })
    .map(function (r) { return [r[1], r[2], r[3], r[4], r[5], r[6], r[0]]; });
  if (rows.length) {
    sh.getRange(2, 1, rows.length, head.length).setValues(rows);
    sh.getRange(2, 7, rows.length, 1).setNumberFormat('d mmm, h:mm am/pm');
    sh.getRange(2, 5, rows.length, 1).setWrap(true);
    colourVerdicts_(sh.getRange(2, 4, rows.length, 1));
    sh.getRange(1, 1, rows.length + 1, head.length).createFilter();
  } else {
    sh.getRange(2, 1).setValue('No comments yet.').setFontColor('#5d6762');
  }
  [110, 120, 230, 110, 420, 130, 130].forEach(function (w, i) { sh.setColumnWidth(i + 1, w); });
  sh.getRange('A:G').setVerticalAlignment('top');
}

function buildByConcept_(ss, data) {
  var sh = ss.getSheetByName(TAB_CONCEPT);
  var keep = sh ? sh.getRange('B2').getValue() : '';
  sh = freshSheet_(ss, TAB_CONCEPT);
  var concepts = unique_(data.map(function (r) { return r[1]; })).sort(function (a, b) { return conceptRank_(a) - conceptRank_(b); });
  sh.getRange('A1').setValue('One concept at a time').setFontSize(14).setFontWeight('bold').setFontColor(HEAD);
  sh.getRange('A2').setValue('Concept:').setFontWeight('bold');
  var pick = sh.getRange('B2');
  pick.setBackground('#fff8e1').setFontWeight('bold').setBorder(true, true, true, true, null, null, '#d39b2a', SpreadsheetApp.BorderStyle.SOLID);
  if (concepts.length) {
    pick.setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(concepts, true).build());
    pick.setValue(concepts.indexOf(keep) > -1 ? keep : concepts[0]);
  }
  sh.getRange('C2').setValue('← choose a concept').setFontColor('#5d6762').setFontStyle('italic');
  var head = ['Page', 'Section', 'Verdict', 'Comment', 'Reviewer', 'Updated'];
  sh.getRange(4, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground(HEAD).setFontColor(HEAD_INK);
  sh.setFrozenRows(4);
  sh.getRange('A5').setFormula("=IFERROR(FILTER({'" + TAB_PICKS + "'!C2:C,'" + TAB_PICKS + "'!D2:D,'" + TAB_PICKS +
    "'!E2:E,'" + TAB_PICKS + "'!F2:F,'" + TAB_PICKS + "'!G2:G,'" + TAB_PICKS + "'!A2:A},'" + TAB_PICKS +
    "'!B2:B=$B$2),\"No picks for this concept yet.\")");
  sh.getRange('F5:F').setNumberFormat('d mmm, h:mm am/pm');
  sh.getRange('D5:D').setWrap(true);
  var c = sh.getRange('C5:C');
  sh.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule().whenTextStartsWith('✓').setBackground(GREEN).setFontColor(GREEN_INK).setRanges([c]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextStartsWith('✕').setBackground(RED).setFontColor(RED_INK).setRanges([c]).build()
  ]);
  [120, 240, 110, 420, 130, 130].forEach(function (w, i) { sh.setColumnWidth(i + 1, w); });
  sh.getRange('A:F').setVerticalAlignment('top');
}

// plain text only: a comment starting with = or + must not become a formula
function text_(v) {
  v = String(v == null ? '' : v).slice(0, 2000);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function unique_(a) {
  var seen = {};
  return a.filter(function (x) { if (!x || seen[x]) return false; seen[x] = true; return true; });
}

/* Run once from the editor to see the layout with sample picks, then use
   "Review > Rebuild the overview" after deleting them from All picks. */
function addSampleData() {
  var now = new Date().toISOString();
  savePicks_([
    { reviewer: 'Sample', reviewerId: 'demo', concept: 'Concept 1', page: 'Homepage', section: 'Hero', verdict: 'Like', comment: 'Love the leaf slideshow', order: 1, key: '/concept-1/#hero', at: now },
    { reviewer: 'Sample', reviewerId: 'demo', concept: 'Concept 1', page: 'Homepage', section: 'Google Reviews', verdict: "Don't like", comment: 'Too much text', order: 7, key: '/concept-1/#google-reviews', at: now },
    { reviewer: 'Sample', reviewerId: 'demo', concept: 'Concept 2', page: 'Homepage', section: 'Hero', verdict: "Don't like", comment: '', order: 1, key: '/concept-2/#hero', at: now }
  ]);
  rebuild();
}
