import json
from pathlib import Path
from flask import (
    render_template, request, redirect,
    url_for, flash, jsonify, session
)

from webapp.services import run_scan, extract_upload, extract_uploads, clone_github_repo, cleanup_temp, validate_uploads
from leakseeker.ai_helper import generate_ai_explanation


def register_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/scan', methods=['POST'])
    def scan():
        scan_path = None
        error = None
        temp_path = None

        try:
            scan_mode = request.form.get('scan_mode', 'upload')
            scan_git = request.form.get('scan_git_history') == 'on'
            min_risk = request.form.get('min_risk', 'low')

            if scan_mode == 'path':
                raw_path = request.form.get('directory_path', '').strip()
                if not raw_path:
                    flash('Please provide a directory path.', 'error')
                    return redirect(url_for('index'))
                scan_path = Path(raw_path).resolve()
                if not scan_path.exists():
                    flash(f"Path does not exist: {scan_path}", 'error')
                    return redirect(url_for('index'))

            elif scan_mode == 'github':
                github_url = request.form.get('github_url', '').strip()
                if not github_url:
                    flash('Please provide a GitHub repository URL.', 'error')
                    return redirect(url_for('index'))
                scan_path = clone_github_repo(github_url)
                temp_path = scan_path

            else:
                files = request.files.getlist('upload_file')
                files = [f for f in files if f and f.filename != '']
                if not files:
                    flash('Please select one or more files to upload.', 'error')
                    return redirect(url_for('index'))
                validate_uploads(files)
                scan_path = extract_uploads(files)
                temp_path = scan_path

            results = run_scan(scan_path, scan_git_history=scan_git, min_risk=min_risk)

            # Store in session (keep it lean — just the findings list)
            session['last_results'] = json.dumps(results['findings'][:500])
            session['last_summary'] = json.dumps(results['summary'])
            session['last_total'] = results['total']
            session['last_risk_score'] = results['risk_score']
            session['last_scan_path'] = str(scan_path)

            return redirect(url_for('results'))

        except Exception as e:
            flash(f'Scan error: {str(e)}', 'error')
            return redirect(url_for('index'))
        finally:
            if temp_path:
                cleanup_temp(temp_path)

    @app.route('/results')
    def results():
        findings_raw = session.get('last_results')
        if not findings_raw:
            flash('No scan results found. Run a scan first.', 'error')
            return redirect(url_for('index'))

        findings = json.loads(findings_raw)
        summary = json.loads(session.get('last_summary', '{}'))
        total = session.get('last_total', 0)
        risk_score = session.get('last_risk_score', 0)
        scan_path = session.get('last_scan_path', '')

        return render_template(
            'results.html',
            findings=findings,
            summary=summary,
            total=total,
            risk_score=risk_score,
            scan_path=scan_path,
        )

    @app.route('/api/explain', methods=['POST'])
    def explain():
        data = request.get_json()
        secret_type = data.get('secret_type', '')
        matched_text = data.get('matched_text', '')
        explanation = generate_ai_explanation(secret_type, matched_text)
        return jsonify({'explanation': explanation})

    @app.route('/api/results')
    def api_results():
        findings_raw = session.get('last_results')
        if not findings_raw:
            return jsonify({'error': 'No results'}), 404
        findings = json.loads(findings_raw)
        summary = json.loads(session.get('last_summary', '{}'))
        return jsonify({
            'findings': findings,
            'summary': summary,
            'total': session.get('last_total', 0),
            'risk_score': session.get('last_risk_score', 0),
        })

