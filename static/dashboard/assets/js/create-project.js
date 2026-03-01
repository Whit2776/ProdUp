// (function(){

//   /* ---------- Helpers ---------- */
//   const $ = (sel, ctx=document) => ctx.querySelector(sel);
//   const $$ = (sel, ctx=document) => Array.from(ctx.querySelectorAll(sel));

//   /* ---------- Steps ---------- */
//   const stepsEl = $('#steps');
//   const steps = $$('.step', stepsEl);
//   let active = 0;

//   const updateUI = () => {
//     steps.forEach((s,i) => {
//       s.classList.toggle('active', i===active);
//       s.setAttribute('aria-hidden', i===active ? 'false' : 'true');
//     });
//     // indicators
//     $$('.indicator').forEach(ind=>{
//       ind.classList.toggle('active', Number(ind.dataset.step)===active);
//     });
//     // progress bar (percent by step)
//     const pct = Math.round(((active) / (steps.length - 1)) * 100);
//     $('#progressBar').style.width = pct + '%';
//     // update review summary
//     updateReview();
//   };

//   // navigation buttons
//   $('#toStep2').addEventListener('click', e => { e.preventDefault(); gotoStep(1); });
//   $('#backTo1').addEventListener('click', e => { e.preventDefault(); gotoStep(0); });
//   $('#toStep3').addEventListener('click', e => { e.preventDefault(); gotoStep(2); });
//   $('#backTo2').addEventListener('click', e => { e.preventDefault(); gotoStep(1); });
//   $('#toStep4').addEventListener('click', e => { e.preventDefault(); gotoStep(3); });
//   $('#backTo3').addEventListener('click', e => { e.preventDefault(); gotoStep(2); });

//   $$('.indicator').forEach(ind=>{
//     ind.addEventListener('click', ()=> gotoStep(Number(ind.dataset.step)));
//   });

//   function gotoStep(i){
//     active = Math.max(0, Math.min(i, steps.length-1));
//     updateUI();
//     if (autosaveEnabled()) autosave(); // save on step change
//   }

//   updateUI();

//   /* ---------- Keyboard shortcuts: Enter to next, Shift+Enter previous ---------- */
//   document.addEventListener('keydown', e=>{
//     if (e.key === 'Enter' && !e.shiftKey && !e.target.matches('textarea')) {
//       e.preventDefault();
//       if (active < steps.length -1) gotoStep(active+1);
//       else $('#createProject').focus();
//     } else if (e.key === 'Enter' && e.shiftKey) {
//       e.preventDefault();
//       if (active > 0) gotoStep(active-1);
//     }
//   });

//   /* ---------- Settings menu & theme ---------- */
//   const settingsBtn = $('#settingsBtn');
//   const settingsMenu = $('#settingsMenu');

//   settingsBtn.addEventListener('click', (e)=>{
//     e.stopPropagation();
//     const show = settingsMenu.classList.toggle('show');
//     settingsBtn.setAttribute('aria-expanded', String(show));
//     settingsMenu.setAttribute('aria-hidden', String(!show));
//   });

//   document.addEventListener('click', (e)=>{
//     if (!settingsMenu.contains(e.target) && e.target !== settingsBtn) {
//       settingsMenu.classList.remove('show');
//       settingsBtn.setAttribute('aria-expanded', 'false');
//     }
//   });

//   // theme options
//   const themeOpt = $$('.theme-option', settingsMenu);
//   const themeApply = (t) => {
//     if (t === 'system') {
//       const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
//       document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
//     } else {
//       document.documentElement.setAttribute('data-theme', t === 'dark' ? 'dark' : 'light');
//     }
//     localStorage.setItem('project_form_theme', t);
//   };
//   themeOpt.forEach(o=>{
//     o.addEventListener('click', ()=> {
//       themeApply(o.dataset.theme);
//       settingsMenu.classList.remove('show');
//     });
//   });

//   // init theme from storage (or system)
//   const savedTheme = localStorage.getItem('project_form_theme') || 'light';
//   themeApply(savedTheme);

//   /* ---------- Autosave ---------- */
//   const autosaveToggle = $('#autosaveToggle');
//   autosaveToggle.addEventListener('change', ()=> {
//     localStorage.setItem('project_form_autosave', autosaveToggle.checked ? '1' : '0');
//     $('#autosaveState').textContent = autosaveToggle.checked ? 'On' : 'Off';
//   });
//   // read initial autosave
//   const autosaveEnabled = () => {
//     const v = localStorage.getItem('project_form_autosave');
//     if (v === null) return true;
//     return v === '1';
//   };
//   autosaveToggle.checked = autosaveEnabled();
//   $('#autosaveState').textContent = autosaveEnabled() ? 'On' : 'Off';

//   // perform autosave
//   function autosave(){
//     if (!autosaveEnabled()) return;
//     const data = gatherFormData();
//     localStorage.setItem('project_form_draft', JSON.stringify(data));
//     // small visual cue could be added here (omitted to stay minimal)
//   }

//   // Save draft / clear / load buttons
//   $('#saveDraft').addEventListener('click', ()=> { autosave(); alert('Draft saved locally'); });
//   $('#clearDraft').addEventListener('click', ()=> {
//     if (confirm('Clear saved draft?')) {
//       localStorage.removeItem('project_form_draft');
//       alert('Draft cleared');
//     }
//   });
//   $('#loadDraft').addEventListener('click', ()=> { loadDraft(); alert('Draft loaded (if present)'); });

//   // autosave every 4 seconds when enabled and form changes
//   let autosaveTimer = null;
//   const startAutosaveTimer = () => {
//     if (autosaveTimer) clearTimeout(autosaveTimer);
//     autosaveTimer = setTimeout(()=>{ if (autosaveEnabled()) autosave(); }, 1500);
//   };

//   // add listeners to fields to trigger autosave timer
//   const inputs = ['#title','#type','#location','#size','#priority','#amount_charged','#budget','#deadline','#notes','#clientInput','#supervisorInput'];
//   inputs.forEach(sel => {
//     const el = $(sel);
//     if (!el) return;
//     el.addEventListener('input', startAutosaveTimer);
//   });

//   /* ---------- Gather & Load form data ---------- */
//   function gatherFormData(){
//     // teams are special chip list
//     const teams = selectedTeams.slice();
//     const file = currentFile ? { name: currentFile.name, size: currentFile.size, type: currentFile.type } : null;
//     return {
//       title: $('#title').value || '',
//       client: $('#clientInput').value || '',
//       type: $('#type').value || '',
//       location: $('#location').value || '',
//       size: $('#size').value || '',
//       priority: $('#priority').value || '',
//       amount_charged: $('#amount_charged').value || '',
//       budget: $('#budget').value || '',
//       deadline: $('#deadline').value || '',
//       notes: $('#notes').value || '',
//       supervisor: $('#supervisorInput').value || '',
//       teams: teams,
//       file: file,
//       activeStep: active
//     };
//   }

//   function loadDraft(){
//     const raw = localStorage.getItem('project_form_draft');
//     if (!raw) return;
//     try {
//       const data = JSON.parse(raw);
//       $('#title').value = data.title || '';
//       $('#clientInput').value = data.client || '';
//       $('#type').value = data.type || '';
//       $('#location').value = data.location || '';
//       $('#size').value = data.size || 'unknown';
//       $('#priority').value = data.priority || 'unknown';
//       $('#amount_charged').value = data.amount_charged || '';
//       $('#budget').value = data.budget || '';
//       $('#deadline').value = data.deadline || '';
//       $('#notes').value = data.notes || '';
//       $('#supervisorInput').value = data.supervisor || '';
//       // teams: re-populate chips (only names stored)
//       if (Array.isArray(data.teams)) {
//         selectedTeams = [];
//         data.teams.forEach(t => addTeamChip(t));
//       }
//       // file: cannot restore binary file; show name only if present
//       if (data.file) {
//         $('#preview').style.display = 'flex';
//         $('#previewImg').src = ''; // no preview
//         $('#previewName').textContent = data.file.name;
//         $('#previewSize').textContent = (data.file.size/1024).toFixed(1) + ' KB (preview not available)';
//       }

//       if (typeof data.activeStep === 'number') {
//         gotoStep(data.activeStep);
//       }
//     } catch(e){}
//   }

//   // try to load on init
//   loadDraft();

//   /* ---------- Searchable selects data (demo dataset) ---------- */
//   // NOTE: Since we have no backend, we provide demo options to search from.
//   const CLIENTS = ['Empower Ltd','Acme Supplies','Greenfield Properties','Zenith Construction','Bright Horizons','Atlas Logistics'];
//   const TEAMS = ['Alpha Team','Bravo Team','Field Ops','Installation','Quality Assurance','Design Studio','Procurement'];
//   const SUPERVISORS = ['Nana Adjei','Josephine Mensah','Kwame Owusu','Aisha Bello','John Smith','Emilia Clarke'];

//   /* ---------- Client search (single) ---------- */
//   const clientInput = $('#clientInput');
//   const clientDropdown = $('#clientDropdown');
//   clientInput.addEventListener('input', ()=> {
//     populateDropdown(clientDropdown, CLIENTS.filter(c=> c.toLowerCase().includes(clientInput.value.toLowerCase())));
//   });
//   clientInput.addEventListener('focus', ()=> {
//     populateDropdown(clientDropdown, CLIENTS);
//     clientDropdown.classList.add('show');
//   });
//   clientInput.addEventListener('blur', ()=> { setTimeout(()=> clientDropdown.classList.remove('show'), 150); });

//   function populateDropdown(container, items){
//     container.innerHTML = '';
//     items.forEach(it=>{
//       const div = document.createElement('div');
//       div.className = 'dropdown-item';
//       div.textContent = it;
//       div.addEventListener('click', ()=> {
//         clientInput.value = it;
//         container.classList.remove('show');
//         if (autosaveEnabled()) autosave();
//       });
//       container.appendChild(div);
//     });
//   }

//   /* ---------- Supervisor search (single) ---------- */
//   const supervisorInput = $('#supervisorInput');
//   const supervisorDropdown = $('#supervisorDropdown');
//   supervisorInput.addEventListener('input', ()=> {
//     populateDropdown(supervisorDropdown, SUPERVISORS.filter(s=> s.toLowerCase().includes(supervisorInput.value.toLowerCase())));
//   });
//   supervisorInput.addEventListener('focus', ()=> {
//     populateDropdown(supervisorDropdown, SUPERVISORS);
//     supervisorDropdown.classList.add('show');
//   });
//   supervisorInput.addEventListener('blur', ()=> { setTimeout(()=> supervisorDropdown.classList.remove('show'), 150); });

//   /* ---------- Team multi-select (chips) ---------- */
//   const teamDropdown = $('#teamDropdown');
//   const teamChips = $('#teamChips');
//   let selectedTeams = [];

//   // initial placeholder element
//   function teamPlaceholder(){ 
//     teamChips.innerHTML = '';
//     const ph = document.createElement('div'); ph.className='small muted'; ph.textContent='Search & add teams...';
//     teamChips.appendChild(ph);
//   }
//   teamPlaceholder();

//   // build dropdown items
//   function populateTeams(filter=''){
//     teamDropdown.innerHTML = '';
//     const items = TEAMS.filter(t => t.toLowerCase().includes(filter.toLowerCase()));
//     items.forEach(it=>{
//       const d = document.createElement('div'); d.className='dropdown-item'; d.textContent = it;
//       d.addEventListener('click', ()=> {
//         if (!selectedTeams.includes(it)) addTeamChip(it);
//         teamDropdown.classList.remove('show');
//         if (autosaveEnabled()) autosave();
//       });
//       teamDropdown.appendChild(d);
//     });
//   }

//   // add chip
//   function addTeamChip(name){
//     if (!name || selectedTeams.includes(name)) return;
//     selectedTeams.push(name);
//     renderTeamChips();
//   }

//   function removeTeamChip(name){
//     selectedTeams = selectedTeams.filter(s=> s !== name);
//     renderTeamChips();
//     if (autosaveEnabled()) autosave();
//   }

//   function renderTeamChips(){
//     teamChips.innerHTML = '';
//     if (selectedTeams.length === 0){
//       teamPlaceholder();
//       return;
//     }
//     selectedTeams.forEach(t=>{
//       const chip = document.createElement('span'); chip.className='chip';
//       chip.textContent = t;
//       const btn = document.createElement('button'); btn.type='button'; btn.textContent='×';
//       btn.addEventListener('click', ()=> removeTeamChip(t));
//       chip.appendChild(btn);
//       teamChips.appendChild(chip);
//     });
//   }

//   // open dropdown when clicking the chips area
//   teamChips.addEventListener('click', (e)=>{
//     populateTeams('');
//     teamDropdown.classList.toggle('show');
//   });

//   // listen for typing to filter teams
//   // create a temporary input for filter
//   const teamFilterInput = document.createElement('input');
//   teamFilterInput.type='text';
//   teamFilterInput.placeholder='Search teams...';
//   teamFilterInput.style.border='none';
//   teamFilterInput.style.outline='none';
//   teamFilterInput.style.flex='1';
//   teamFilterInput.style.minWidth='120px';
//   teamFilterInput.style.padding='8px';
//   teamFilterInput.addEventListener('input', ()=> populateTeams(teamFilterInput.value));
//   teamFilterInput.addEventListener('keydown', (e)=>{
//     if (e.key === 'Enter') {
//       if (teamFilterInput.value.trim()) addTeamChip(teamFilterInput.value.trim());
//       teamFilterInput.value='';
//       teamDropdown.classList.remove('show');
//     }
//   });

//   // inject the filter input into the dropdown wrapper when opened
//   teamDropdown.addEventListener('mouseenter', ()=> {
//     if (!teamDropdown.querySelector('input')) {
//       const wrapper = document.createElement('div'); wrapper.style.padding='6px';
//       wrapper.appendChild(teamFilterInput);
//       teamDropdown.insertBefore(wrapper, teamDropdown.firstChild);
//     }
//   });

//   // hide dropdown on outside click
//   document.addEventListener('click', (e)=> {
//     if (!teamChips.contains(e.target) && !teamDropdown.contains(e.target)) {
//       teamDropdown.classList.remove('show');
//     }
//   });

//   /* ---------- Drag & Drop file upload ---------- */
//   const dropzone = $('#dropzone');
//   const fileInput = $('#fileInput');
//   const preview = $('#preview');
//   const previewImg = $('#previewImg');
//   const previewName = $('#previewName');
//   const previewSize = $('#previewSize');
//   const removeFileBtn = $('#removeFile');
//   let currentFile = null;

//   dropzone.addEventListener('click', ()=> fileInput.click());
//   fileInput.addEventListener('change', ()=> {
//     if (fileInput.files && fileInput.files[0]) handleFile(fileInput.files[0]);
//   });

//   dropzone.addEventListener('dragover', (e)=> {
//     e.preventDefault(); dropzone.classList.add('dragover');
//   });
//   dropzone.addEventListener('dragleave', ()=> dropzone.classList.remove('dragover'));
//   dropzone.addEventListener('drop', (e)=> {
//     e.preventDefault(); dropzone.classList.remove('dragover');
//     const f = e.dataTransfer.files && e.dataTransfer.files[0];
//     if (f) handleFile(f);
//   });

//   function handleFile(file){
//     if (!file.type.startsWith('image/')) { alert('Only images allowed'); return; }
//     if (file.size > 5 * 1024 * 1024) { if (!confirm('File is large (>5MB). Continue?')) return; }
//     currentFile = file;
//     const reader = new FileReader();
//     reader.onload = (ev) => {
//       previewImg.src = ev.target.result;
//       preview.style.display = 'flex';
//       previewName.textContent = file.name;
//       previewSize.textContent = (file.size/1024).toFixed(1) + ' KB';
//       if (autosaveEnabled()) autosave();
//     };
//     reader.readAsDataURL(file);
//   }

//   removeFileBtn.addEventListener('click', (e)=> {
//     e.preventDefault();
//     currentFile = null;
//     fileInput.value = '';
//     preview.style.display = 'none';
//     previewImg.src = '';
//     if (autosaveEnabled()) autosave();
//   });

//   /* ---------- Review summary ---------- */
//   function updateReview(){
//     const d = gatherFormData();
//     const lines = [];
//     if (d.title) lines.push('<strong>Title:</strong> ' + escapeHtml(d.title));
//     if (d.client) lines.push('<strong>Client:</strong> ' + escapeHtml(d.client));
//     if (d.teams && d.teams.length) lines.push('<strong>Teams:</strong> ' + escapeHtml(d.teams.join(', ')));
//     if (d.supervisor) lines.push('<strong>Supervisor:</strong> ' + escapeHtml(d.supervisor));
//     if (d.amount_charged) lines.push('<strong>Amount:</strong> GHC ' + escapeHtml(d.amount_charged));
//     if (d.budget) lines.push('<strong>Budget:</strong> GHC ' + escapeHtml(d.budget));
//     if (d.deadline) lines.push('<strong>Deadline:</strong> ' + escapeHtml(d.deadline));
//     if (!lines.length) lines.push('No fields filled yet');
//     $('#reviewSummary').innerHTML = lines.join('<br>');
//   }

//   function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])); }

//   /* ---------- Create Project (final action) ---------- */
//   $('#createProject').addEventListener('click', (e)=> {
//     e.preventDefault();
//     // minimal validation: title required
//     if (!$('#title').value.trim()) {
//       alert('Please provide a project title.');
//       gotoStep(0);
//       $('#title').focus();
//       return;
//     }

//     // gather data
//     const data = gatherFormData();
//     // Since there's no backend, we'll simulate a submission.
//     // In real setup, you'd POST data and the file via FormData.
//     localStorage.setItem('project_form_last_submission', JSON.stringify(Object.assign({}, data, { submittedAt: new Date().toISOString() })));
//     alert('Project created (simulated). Draft cleared.');
//     localStorage.removeItem('project_form_draft');
//     // reset form visually
//     resetForm();
//   });

//   function resetForm(){
//     // clear inputs
//     ['#title','#clientInput','#type','#location','#amount_charged','#budget','#deadline','#notes','#supervisorInput'].forEach(sel=>{
//       const el = $(sel); if (el) el.value = '';
//     });
//     selectedTeams = []; renderTeamChips();
//     currentFile = null; preview.style.display = 'none'; previewImg.src = '';
//     gotoStep(0);
//     updateReview();
//   }

//   /* ---------- Save / Load initial sample lists into dropdowns (for UX) ---------- */
//   // Prepopulate client dropdown so clicking input shows options
//   populateDropdown(clientDropdown, CLIENTS);
//   populateTeams('');
//   populateDropdown(supervisorDropdown, SUPERVISORS);

//   /* ---------- utility: small debounce to autosave when many events happen ---------- */
//   let deb = null;
//   document.addEventListener('input', ()=> {
//     if (deb) clearTimeout(deb);
//     deb = setTimeout(()=> { if (autosaveEnabled()) autosave(); }, 900);
//   });

//   // also autosave on unload
//   window.addEventListener('beforeunload', ()=> { if (autosaveEnabled()) autosave(); });

//   // initial UI update
//   updateUI();

// })();

$(document).ready(function() {
  let currentStep = 0;
  const totalSteps = $(".step").length - 1;


  // Show only the first section initially
  // $(".step").hide();
  $(`.step[data-step="${currentStep}"]`).show();
  updateIndicators();

  // ==== NEXT BUTTON ====
  let progressBar = document.querySelector('#progressBar')
  let width = 25
  $(".next").click(function() {
    if (currentStep <= totalSteps) {
      console.log(width)
      $(`.step[data-step="${currentStep}"]`).hide();
      currentStep++;
      $(`.step[data-step="${currentStep}"]`).fadeIn(200);
      updateIndicators();

      width = width + 25
      progressBar.style.width = width+'%'

    } else{
      currentStep = 0
    }
  });

  // ==== PREVIOUS BUTTON ====
  $(".back").click(function() {
    if (currentStep >= 0) {
      $(`.step[data-step="${currentStep}"]`).hide();
      currentStep--;
      $(`.step[data-step="${currentStep}"]`).fadeIn(200);
      updateIndicators();

      width = width - 25
      progressBar.style.width = width+'%'
    }
  });
  
  // ==== CLICK STEP INDICATOR ====
  $(".indicator").click(function() {
    const target = $(this).data("step");
    if (target >= 0 && target <= totalSteps) {
      $(`.step[data-step="${currentStep}"]`).hide();
      currentStep = target;
      $(`.step[data-step="${currentStep}"]`).fadeIn(200);
      updateIndicators();
    }

    if(target === 0){
      width = 25
      progressBar.style.width = width+'%'
    } else if(target === 1){
      width = 50
      progressBar.style.width = width+'%'
    } else if(target === 2){
      width = 75
      progressBar.style.width = width+'%'
    } else if(target === 3){
      width = 100
      progressBar.style.width = width+'%'
    }
  });

  // ==== UPDATE INDICATOR UI ====
  function updateIndicators() {
      $(".indicator").removeClass("active visited");

      // Mark visited ones
      $(".indicator").each(function() {
          if ($(this).data("step") < currentStep) {
              $(this).addClass("visited");
          }
      });

      // Mark current
      $(`.indicator[data-step="${currentStep}"]`).addClass("active");
  }
});
