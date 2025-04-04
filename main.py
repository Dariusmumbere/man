<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NGO Management System</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2980b9;
            --accent-color: #e74c3c;
            --light-color: #ecf0f1;
            --dark-color: #2c3e50;
            --success-color: #2ecc71;
            --warning-color: #f39c12;
            --sidebar-width: 250px;
            --sidebar-collapsed-width: 80px;
            --header-height: 70px;
            --transition-speed: 0.3s;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #f5f7fa;
            color: #333;
            overflow-x: hidden;
        }

        .container {
            display: flex;
            min-height: 100vh;
            transition: margin-left var(--transition-speed);
        }

        /* Header Styles */
        header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 100;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo img {
            height: 40px;
        }

        .logo h1 {
            font-size: 1.2rem;
            color: var(--dark-color);
            font-weight: 700;
            white-space: nowrap;
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .user-profile img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }

        .user-info {
            display: flex;
            flex-direction: column;
        }

        .user-name {
            font-weight: 600;
            font-size: 0.9rem;
        }

        .user-role {
            font-size: 0.8rem;
            color: #777;
        }

        /* Sidebar Styles */
        .sidebar {
            position: fixed;
            top: var(--header-height);
            left: 0;
            width: var(--sidebar-width);
            height: calc(100vh - var(--header-height));
            background-color: var(--dark-color);
            color: white;
            transition: width var(--transition-speed);
            overflow: hidden;
            z-index: 99;
        }

        .sidebar.collapsed {
            width: var(--sidebar-collapsed-width);
        }

        .sidebar-menu {
            list-style: none;
            padding: 20px 0;
        }

        .sidebar-menu li {
            position: relative;
        }

        .sidebar-menu li a {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            color: var(--light-color);
            text-decoration: none;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .sidebar-menu li a:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .sidebar-menu li a.active {
            background-color: var(--primary-color);
        }

        .sidebar-menu li a i {
            font-size: 1.2rem;
            margin-right: 15px;
            min-width: 24px;
            text-align: center;
        }

        .sidebar-menu li a span {
            transition: opacity var(--transition-speed);
        }

        .sidebar.collapsed .sidebar-menu li a span {
            opacity: 0;
            width: 0;
            display: none;
        }

        .sidebar.collapsed .sidebar-menu li a {
            justify-content: center;
            padding: 15px 0;
        }

        .sidebar.collapsed .sidebar-menu li a i {
            margin-right: 0;
        }

        .submenu {
            list-style: none;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            background-color: rgba(0, 0, 0, 0.2);
        }

        .submenu.show {
            max-height: 500px;
        }

        .submenu li a {
            padding-left: 50px !important;
            font-size: 0.9rem;
        }

        .sidebar.collapsed .submenu li a {
            padding-left: 0 !important;
            justify-content: center;
        }

        .menu-toggle {
            background: none;
            border: none;
            color: var(--dark-color);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 10px;
        }

        /* Main Content Styles */
        .main-content {
            flex: 1;
            margin-left: var(--sidebar-width);
            margin-top: var(--header-height);
            padding: 30px;
            transition: margin-left var(--transition-speed);
        }

        .sidebar.collapsed ~ .main-content {
            margin-left: var(--sidebar-collapsed-width);
        }

        .page-title {
            font-size: 1.8rem;
            color: var(--dark-color);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Dashboard Styles */
        .stats-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }

        .stat-card .stat-title {
            font-size: 0.9rem;
            color: #777;
            margin-bottom: 10px;
        }

        .stat-card .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .stat-card .stat-change {
            display: flex;
            align-items: center;
            font-size: 0.9rem;
        }

        .stat-card .stat-change.positive {
            color: var(--success-color);
        }

        .stat-card .stat-change.negative {
            color: var(--accent-color);
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }

        .dashboard-section {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark-color);
        }

        .section-link {
            color: var(--primary-color);
            font-size: 0.9rem;
            text-decoration: none;
        }

        .recent-activities {
            list-style: none;
        }

        .activity-item {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .activity-item:last-child {
            border-bottom: none;
        }

        .activity-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: var(--light-color);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: var(--primary-color);
        }

        .activity-content {
            flex: 1;
        }

        .activity-title {
            font-weight: 600;
            margin-bottom: 5px;
        }

        .activity-time {
            font-size: 0.8rem;
            color: #777;
        }

        .project-progress {
            margin-top: 20px;
        }

        .project-item {
            margin-bottom: 15px;
        }

        .project-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }

        .project-name {
            font-weight: 600;
        }

        .project-percent {
            color: var(--primary-color);
        }

        .progress-bar {
            height: 8px;
            background-color: #eee;
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background-color: var(--primary-color);
            border-radius: 4px;
        }

        .donation-chart {
            height: 250px;
            margin-top: 20px;
        }

        /* Enhanced File Manager Styles */
        .file-manager-container {
            display: none;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
        }

        .file-manager-container.show {
            display: block;
        }

        .file-manager-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .file-manager-actions {
            display: flex;
            gap: 10px;
        }

        .file-manager-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .file-manager-btn:hover {
            background-color: var(--secondary-color);
        }

        .file-manager-btn.secondary {
            background-color: #f0f0f0;
            color: var(--dark-color);
        }

        .file-manager-btn.secondary:hover {
            background-color: #e0e0e0;
        }

        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }

        .breadcrumb-item {
            color: var(--primary-color);
            cursor: pointer;
        }

        .breadcrumb-item:hover {
            text-decoration: underline;
        }

        .breadcrumb-separator {
            color: #777;
        }

        .file-manager-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 15px;
        }

        .file-item, .folder-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }

        .file-item:hover, .folder-item:hover {
            background-color: #f5f5f5;
        }

        .file-icon, .folder-icon {
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
            color: var(--primary-color);
            font-size: 2rem;
        }

        .folder-icon {
            color: var(--warning-color);
        }

        .file-name, .folder-name {
            text-align: center;
            font-size: 0.8rem;
            font-weight: 500;
            word-break: break-word;
            width: 100%;
        }

        .file-actions-menu {
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: white;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            opacity: 0;
            transition: opacity 0.2s;
        }

        .file-item:hover .file-actions-menu,
        .folder-item:hover .file-actions-menu {
            opacity: 1;
        }

        .file-actions-dropdown {
            position: absolute;
            top: 30px;
            right: 0;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 10;
            display: none;
            min-width: 150px;
        }

        .file-actions-dropdown.show {
            display: block;
        }

        .file-action-item {
            padding: 8px 15px;
            font-size: 0.85rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .file-action-item:hover {
            background-color: #f5f5f5;
        }

        .file-action-item i {
            width: 18px;
            text-align: center;
        }

        .file-preview-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .file-preview-modal.show {
            opacity: 1;
            visibility: visible;
        }

        .file-preview-content {
            background-color: white;
            border-radius: 10px;
            width: 80%;
            max-width: 900px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
        }

        .file-preview-header {
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .file-preview-body {
            flex: 1;
            padding: 20px;
            overflow: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .file-preview-iframe {
            width: 100%;
            height: 60vh;
            border: none;
            background-color: #f9f9f9;
        }

        .file-preview-image {
            max-width: 100%;
            max-height: 60vh;
            object-fit: contain;
        }

        .file-preview-actions {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }

        .folder-create-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .folder-create-modal.show {
            opacity: 1;
            visibility: visible;
        }

        .folder-create-content {
            background-color: white;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
            padding: 20px;
        }

        .folder-create-header {
            margin-bottom: 20px;
        }

        .folder-create-body {
            margin-bottom: 20px;
        }

        .folder-create-input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }

        .folder-create-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }

        /* Upload Modal Styles */
        .upload-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .upload-modal.show {
            opacity: 1;
            visibility: visible;
        }

        .upload-content {
            background-color: white;
            border-radius: 10px;
            width: 90%;
            max-width: 600px;
            padding: 20px;
        }

        .upload-header {
            margin-bottom: 20px;
        }

        .upload-area {
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }

        .upload-area:hover {
            border-color: var(--primary-color);
            background-color: rgba(52, 152, 219, 0.05);
        }

        .upload-area i {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }

        .upload-area p {
            margin-bottom: 10px;
            color: #777;
        }

        .upload-area .browse-btn {
            color: var(--primary-color);
            font-weight: 600;
            cursor: pointer;
        }

        #fileUploadInput {
            display: none;
        }

        .upload-progress {
            margin-top: 15px;
            display: none;
        }

        .progress-bar-container {
            width: 100%;
            height: 10px;
            background-color: #eee;
            border-radius: 5px;
            margin-top: 10px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background-color: var(--primary-color);
            width: 0%;
            transition: width 0.3s;
        }

        .upload-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 20px;
        }

        /* Responsive adjustments */
        @media (max-width: 992px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .logo h1 {
                font-size: 1rem;
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform var(--transition-speed);
            }

            .sidebar.show {
                transform: translateX(0);
            }

            .sidebar.collapsed {
                width: var(--sidebar-width);
            }

            .main-content {
                margin-left: 0;
            }
            
            .logo h1 {
                display: none;
            }
        }

            .file-manager-grid {
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            }
            
            .file-preview-content {
                width: 95%;
                height: 90vh;
            }

            .file-manager-actions {
                flex-direction: column;
                align-items: flex-end;
            }
        }
                /* Donations Page Styles */
        .donations-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }

        .donations-tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }

        .tab-btn {
            padding: 10px 20px;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-weight: 600;
            color: #777;
            transition: all 0.3s;
        }

        .tab-btn.active {
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
        }

        .tab-btn:hover:not(.active) {
            color: var(--dark-color);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .table-responsive {
            overflow-x: auto;
        }

        .donations-table {
            width: 100%;
            border-collapse: collapse;
        }

        .donations-table th, 
        .donations-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .donations-table th {
            background-color: #f9f9f9;
            font-weight: 600;
        }

        .donations-table tr:hover {
            background-color: #f5f5f5;
        }

        .status-badge {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .status-badge.completed {
            background-color: #e6f7ee;
            color: var(--success-color);
        }

        .status-badge.pending {
            background-color: #fff5e6;
            color: var(--warning-color);
        }

        .action-btn {
            background: none;
            border: none;
            cursor: pointer;
            padding: 5px;
            margin: 0 3px;
            color: #777;
            transition: color 0.2s;
        }

        .action-btn:hover {
            color: var(--primary-color);
        }

        .action-btn.delete-btn:hover {
            color: var(--accent-color);
        }

        .receipts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .receipt-card {
            border: 1px solid #eee;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .receipt-header {
            background-color: #f9f9f9;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #eee;
        }

        .receipt-header h3 {
            margin: 0;
            font-size: 1.1rem;
        }

        .receipt-date {
            color: #777;
            font-size: 0.9rem;
        }

        .receipt-body {
            padding: 15px;
        }

        .receipt-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .receipt-row:last-child {
            margin-bottom: 0;
        }

        .receipt-label {
            font-weight: 600;
            color: #555;
        }

        .receipt-value {
            text-align: right;
        }

        .receipt-actions {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }

        .donor-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .donor-card {
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 20px;
            display: flex;
            gap: 15px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .donor-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: var(--primary-color);
            flex-shrink: 0;
        }

        .donor-info {
            flex: 1;
        }

        .donor-name {
            margin: 0 0 10px 0;
            font-size: 1.2rem;
        }

        .donor-contact {
            display: flex;
            flex-direction: column;
            gap: 5px;
            margin-bottom: 15px;
            font-size: 0.9rem;
            color: #555;
        }

        .donor-contact i {
            width: 20px;
            text-align: center;
        }

        .donor-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .stat-item {
            font-size: 0.9rem;
        }

        .stat-label {
            display: block;
            color: #777;
            font-size: 0.8rem;
        }

        .stat-value {
            font-weight: 600;
        }

        .donor-actions {
            display: flex;
            flex-direction: column;
            gap: 10px;
            justify-content: center;
        }

        /* Donation Modal Styles */
        .donation-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .donation-modal.show {
            opacity: 1;
            visibility: visible;
        }

        .modal-content {
            background-color: white;
            border-radius: 8px;
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
        }

        .modal-header {
            padding: 15px 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h3 {
            margin: 0;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #777;
        }

        .modal-body {
            padding: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }

        .form-group textarea {
            resize: vertical;
        }

        .modal-footer {
            padding: 15px 20px;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        /* Add to your existing CSS */
.donor-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s;
}

.donor-modal.show {
    opacity: 1;
    visibility: visible;
}

.donor-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 20px;
}

.stat-item {
    font-size: 0.9rem;
}

.stat-label {
    display: block;
    color: #777;
    font-size: 0.8rem;
}

.stat-value {
    font-weight: 600;
}
    </style>
</head>
<body>
    <header>
        <div class="logo">
            <button class="menu-toggle" id="menuToggle">
                <i class="fas fa-bars"></i>
            </button>
            <img src="logo.jpg" alt="RWENZORI COMMUNITY DEVELOPMENT NETWORK Logo">
            <h1>RWENZORI COMMUNITY DEVELOPMENT NETWORK(RCDNET)</h1>
        </div>
        <div class="user-profile">
            <div class="user-info">
                <span class="user-name">Ndyakurungi Mugisha</span>
                <span class="user-role">Chief Executive Director</span>
            </div>
            <img src="mugisha.png" alt="User Profile">
        </div>
    </header>

    <div class="container">
        <aside class="sidebar" id="sidebar">
            <ul class="sidebar-menu">
                <li>
                    <a href="#" class="active" id="dashboardLink">
                        <i class="fas fa-tachometer-alt"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="fas fa-comments"></i>
                        <span>Chat</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="fas fa-bullhorn"></i>
                        <span>Notice Board</span>
                    </a>
                </li>
                <li>
                    <a href="#" id="fundraisingLink">
                        <i class="fas fa-file-invoice-dollar"></i>
                        <span>Fundraising Documents</span>
                    </a>
                </li>
                <li>
    <a href="#" id="donationsLink">
        <i class="fas fa-hand-holding-usd"></i>
        <span>Collect Donations</span>
    </a>
</li>
                <li>
                    <a href="#" class="has-submenu" id="reportsMenu">
                        <i class="fas fa-chart-pie"></i>
                        <span>Project management</span>
                        <i class="fas fa-chevron-down ml-auto" id="reportsArrow"></i>
                    </a>
                    <ul class="submenu" id="reportsSubmenu">
                        <li><a href="#"><span>Create New Project</span></a></li>
                        <li><a href="#"><span>Implement Project</span></a></li>
                        <li><a href="#"><span>Project Report</span></a></li>
                        <li><a href="#"><span>Staff</span></a></li>
                        <li><a href="#"><span>Budget</span></a></li>
                        <li><a href="#"><span>Payments</span></a></li>
                        <li><a href="#"><span>Accountability</span></a></li>
                    </ul>
                </li>
                <li>
                    <a href="#">
                        <i class="fas fa-users"></i>
                        <span>Beneficiaries</span>
                    </a>
                </li>
                <li>
                    <a href="#">
                        <i class="fas fa-file-alt"></i>
                        <span>Reports</span>
                    </a>
                </li>
                
            </ul>
        </aside>

        <main class="main-content" id="mainContent">
            <!-- Dashboard Content -->
            <div id="dashboardContent">
                <h1 class="page-title">
                    <i class="fas fa-tachometer-alt"></i>
                    Dashboard
                </h1>

                <div class="stats-cards">
                    <div class="stat-card">
                        <div class="stat-title">Total Donations</div>
                        <div class="stat-value">UGX 20,000,000</div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> 12% from last month
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">Active Projects</div>
                        <div class="stat-value">8</div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> 2 new this month
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">Beneficiaries</div>
                        <div class="stat-value">1,500</div>
                        <div class="stat-change positive">
                            <i class="fas fa-arrow-up"></i> 5% from last quarter
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">Volunteers</div>
                        <div class="stat-value">42</div>
                        <div class="stat-change negative">
                            <i class="fas fa-arrow-down"></i> 2 left this month
                        </div>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <div class="dashboard-section">
                        <div class="section-header">
                            <h2 class="section-title">Recent Activities</h2>
                            <a href="#" class="section-link">View All</a>
                        </div>
                        <ul class="recent-activities">
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-donate"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">New donation received from KELA Foundation</div>
                                    <div class="activity-time">2 hours ago</div>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-user-plus"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">3 new volunteers joined the team</div>
                                    <div class="activity-time">Yesterday</div>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-check-circle"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Education project phase 1 completed</div>
                                    <div class="activity-time">2 days ago</div>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-calendar-alt"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Upcoming fundraising event scheduled</div>
                                    <div class="activity-time">3 days ago</div>
                                </div>
                            </li>
                            <li class="activity-item">
                                <div class="activity-icon">
                                    <i class="fas fa-file-alt"></i>
                                </div>
                                <div class="activity-content">
                                    <div class="activity-title">Monthly report submitted to board</div>
                                    <div class="activity-time">1 week ago</div>
                                </div>
                            </li>
                        </ul>
                    </div>

                    <div class="dashboard-section">
                        <div class="section-header">
                            <h2 class="section-title">Project Progress</h2>
                            <a href="#" class="section-link">View All</a>
                        </div>
                        <div class="project-progress">
                            <div class="project-item">
                                <div class="project-header">
                                    <span class="project-name">Agriculture Extension Model Services and Market Linkages</span>
                                    <span class="project-percent">75%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 75%"></div>
                                </div>
                            </div>
                            <div class="project-item">
                                <div class="project-header">
                                    <span class="project-name">Vocation Education & Entrepreneurship</span>
                                    <span class="project-percent">42%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 42%"></div>
                                </div>
                            </div>
                            <div class="project-item">
                                <div class="project-header">
                                    <span class="project-name">Women Empowerment</span>
                                    <span class="project-percent">90%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 90%"></div>
                                </div>
                            </div>
                            <div class="project-item">
                                <div class="project-header">
                                    <span class="project-name">Economic empowerment</span>
                                    <span class="project-percent">28%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 28%"></div>
                                </div>
                            </div>
                        </div>

                        <div class="section-header" style="margin-top: 30px;">
                            <h2 class="section-title">Donation Sources</h2>
                        </div>
                        <div class="donation-chart">
                            <div style="display: flex; height: 100%; align-items: flex-end; justify-content: space-around;">
                                <div style="width: 15%; background-color: var(--primary-color); height: 70%; border-radius: 5px 5px 0 0;"></div>
                                <div style="width: 15%; background-color: var(--success-color); height: 40%; border-radius: 5px 5px 0 0;"></div>
                                <div style="width: 15%; background-color: var(--accent-color); height: 60%; border-radius: 5px 5px 0 0;"></div>
                                <div style="width: 15%; background-color: var(--warning-color); height: 30%; border-radius: 5px 5px 0 0;"></div>
                                <div style="width: 15%; background-color: var(--secondary-color); height: 80%; border-radius: 5px 5px 0 0;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top: 10px;">
                                <span style="font-size: 0.8rem;">Individuals</span>
                                <span style="font-size: 0.8rem;">Corporates</span>
                                <span style="font-size: 0.8rem;">Grants</span>
                                <span style="font-size: 0.8rem;">Events</span>
                                <span style="font-size: 0.8rem;">Other</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Enhanced File Manager Content -->
            <div id="fileManagerContent" class="file-manager-container">
                <div class="file-manager-header">
                    <h1 class="page-title">
                        <i class="fas fa-folder-open"></i>
                        Fundraising Documents
                    </h1>
                    <div class="file-manager-actions">
                        <button class="file-manager-btn" id="uploadFilesBtn">
                            <i class="fas fa-upload"></i> Upload
                        </button>
                        <button class="file-manager-btn secondary" id="createFolderBtn">
                            <i class="fas fa-folder-plus"></i> New Folder
                        </button>
                    </div>
                </div>

                <div class="breadcrumb" id="breadcrumb">
                    <span class="breadcrumb-item" data-path="">Fundraising Documents</span>
                </div>

                <div class="file-manager-grid" id="fileManagerGrid">
                    <!-- Folders will be added here -->
                    <div class="folder-item" data-folder-id="1" data-folder-name="Proposals">
                        <div class="folder-icon">
                            <i class="fas fa-folder"></i>
                        </div>
                        <div class="folder-name">Proposals</div>
                        <div class="file-actions-menu" onclick="toggleFolderActions(event, 1)">
                            <i class="fas fa-ellipsis-v"></i>
                        </div>
                        <div class="file-actions-dropdown" id="folder-actions-1">
                            <div class="file-action-item" onclick="renameFolder(1, 'Proposals')">
                                <i class="fas fa-pencil-alt"></i> Rename
                            </div>
                            <div class="file-action-item" onclick="deleteFolder(1)">
                                <i class="fas fa-trash"></i> Delete
                            </div>
                        </div>
                    </div>

                    <div class="folder-item" data-folder-id="2" data-folder-name="Reports">
                        <div class="folder-icon">
                            <i class="fas fa-folder"></i>
                        </div>
                        <div class="folder-name">Reports</div>
                        <div class="file-actions-menu" onclick="toggleFolderActions(event, 2)">
                            <i class="fas fa-ellipsis-v"></i>
                        </div>
                        <div class="file-actions-dropdown" id="folder-actions-2">
                            <div class="file-action-item" onclick="renameFolder(2, 'Reports')">
                                <i class="fas fa-pencil-alt"></i> Rename
                            </div>
                            <div class="file-action-item" onclick="deleteFolder(2)">
                                <i class="fas fa-trash"></i> Delete
                            </div>
                        </div>
                    </div>

                    <!-- Files will be added here -->
                    <div class="file-item" data-file-id="1" data-file-name="Annual_Report_2023.pdf">
                        <div class="file-icon">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="file-name">Annual_Report_2023.pdf</div>
                        <div class="file-actions-menu" onclick="toggleFileActions(event, 1)">
                            <i class="fas fa-ellipsis-v"></i>
                        </div>
                        <div class="file-actions-dropdown" id="file-actions-1">
                            <div class="file-action-item" onclick="previewFile(1, 'Annual_Report_2023.pdf', 'pdf')">
                                <i class="fas fa-eye"></i> Preview
                            </div>
                            <div class="file-action-item" onclick="downloadFile(1, 'Annual_Report_2023.pdf')">
                                <i class="fas fa-download"></i> Download
                            </div>
                            <div class="file-action-item" onclick="renameFile(1, 'Annual_Report_2023.pdf')">
                                <i class="fas fa-pencil-alt"></i> Rename
                            </div>
                            <div class="file-action-item" onclick="deleteFile(1, 'Annual_Report_2023.pdf')">
                                <i class="fas fa-trash"></i> Delete
                            </div>
                        </div>
                    </div>

                    <div class="file-item" data-file-id="2" data-file-name="Budget_2024.xlsx">
                        <div class="file-icon">
                            <i class="fas fa-file-excel"></i>
                        </div>
                        <div class="file-name">Budget_2024.xlsx</div>
                        <div class="file-actions-menu" onclick="toggleFileActions(event, 2)">
                            <i class="fas fa-ellipsis-v"></i>
                        </div>
                        <div class="file-actions-dropdown" id="file-actions-2">
                            <div class="file-action-item" onclick="previewFile(2, 'Budget_2024.xlsx', 'xlsx')">
                                <i class="fas fa-eye"></i> Preview
                            </div>
                            <div class="file-action-item" onclick="downloadFile(2, 'Budget_2024.xlsx')">
                                <i class="fas fa-download"></i> Download
                            </div>
                            <div class="file-action-item" onclick="renameFile(2, 'Budget_2024.xlsx')">
                                <i class="fas fa-pencil-alt"></i> Rename
                            </div>
                            <div class="file-action-item" onclick="deleteFile(2, 'Budget_2024.xlsx')">
                                <i class="fas fa-trash"></i> Delete
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                        <!-- Donations Collection Content -->
            <div id="donationsContent" class="donations-container" style="display: none;">
                <h1 class="page-title">
                    <i class="fas fa-hand-holding-usd"></i>
                    Collect Donations
                </h1>

                <div class="donations-tabs">
                    <button class="tab-btn active" data-tab="donationHistory">Donations</button>
                    <button class="tab-btn" data-tab="receipts">Receipts/Invoices</button>
                    <button class="tab-btn" data-tab="donorProfiles">Donor Profiles</button>
                </div>

                <div class="tab-content active" id="donationHistory">
                    <div class="section-header">
                        <h2 class="section-title">Recent Donations</h2>
                        <button class="file-manager-btn" id="addDonationBtn">
                            <i class="fas fa-plus"></i> Add Donation
                        </button>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="donations-table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Donor</th>
                                    <th>Amount</th>
                                    <th>Payment Method</th>
                                    <th>Campaign/Project</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>2023-10-15</td>
                                    <td>JMumbere Darius</td>
                                    <td>UGX 500,000</td>
                                    <td>Mobile Money</td>
                                    <td>Agriculture Extension</td>
                                    <td><span class="status-badge completed">Completed</span></td>
                                    <td>
                                        <button class="action-btn view-btn"><i class="fas fa-eye"></i></button>
                                        <button class="action-btn edit-btn"><i class="fas fa-edit"></i></button>
                                        <button class="action-btn delete-btn"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>2023-10-10</td>
                                    <td>Acme Corp</td>
                                    <td>UGX 2,000,000</td>
                                    <td>Bank Transfer</td>
                                    <td>Vocational Education</td>
                                    <td><span class="status-badge completed">Completed</span></td>
                                    <td>
                                        <button class="action-btn view-btn"><i class="fas fa-eye"></i></button>
                                        <button class="action-btn edit-btn"><i class="fas fa-edit"></i></button>
                                        <button class="action-btn delete-btn"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>2023-10-05</td>
                                    <td>Ndyakurungi Mugisha</td>
                                    <td>UGX 250,000</td>
                                    <td>PayPal</td>
                                    <td>Women Empowerment</td>
                                    <td><span class="status-badge pending">Pending</span></td>
                                    <td>
                                        <button class="action-btn view-btn"><i class="fas fa-eye"></i></button>
                                        <button class="action-btn edit-btn"><i class="fas fa-edit"></i></button>
                                        <button class="action-btn delete-btn"><i class="fas fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="tab-content" id="receipts">
                    <div class="section-header">
                        <h2 class="section-title">Generate Receipts/Invoices</h2>
                    </div>
                    
                    <div class="receipts-grid">
                        <div class="receipt-card">
                            <div class="receipt-header">
                                <h3>Donation Receipt</h3>
                                <span class="receipt-date">2023-10-15</span>
                            </div>
                            <div class="receipt-body">
                                <div class="receipt-row">
                                    <span class="receipt-label">Donor:</span>
                                    <span class="receipt-value">Mumbere Darius</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Amount:</span>
                                    <span class="receipt-value">UGX 500,000</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Payment Method:</span>
                                    <span class="receipt-value">Mobile Money</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Purpose:</span>
                                    <span class="receipt-value">Agriculture Extension</span>
                                </div>
                            </div>
                            <div class="receipt-actions">
                                <button class="file-manager-btn"><i class="fas fa-download"></i> Download PDF</button>
                                <button class="file-manager-btn secondary"><i class="fas fa-envelope"></i> Email Receipt</button>
                            </div>
                        </div>
                        
                        <div class="receipt-card">
                            <div class="receipt-header">
                                <h3>Donation Receipt</h3>
                                <span class="receipt-date">2023-10-10</span>
                            </div>
                            <div class="receipt-body">
                                <div class="receipt-row">
                                    <span class="receipt-label">Donor:</span>
                                    <span class="receipt-value">Acme Corp</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Amount:</span>
                                    <span class="receipt-value">UGX 2,000,000</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Payment Method:</span>
                                    <span class="receipt-value">Bank Transfer</span>
                                </div>
                                <div class="receipt-row">
                                    <span class="receipt-label">Purpose:</span>
                                    <span class="receipt-value">Vocational Education</span>
                                </div>
                            </div>
                            <div class="receipt-actions">
                                <button class="file-manager-btn"><i class="fas fa-download"></i> Download PDF</button>
                                <button class="file-manager-btn secondary"><i class="fas fa-envelope"></i> Email Receipt</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-content" id="donorProfiles">
                    <div class="section-header">
                        <h2 class="section-title">Donor Profiles</h2>
                        <button class="file-manager-btn" id="addDonorBtn">
                            <i class="fas fa-plus"></i> Add Donor
                        </button>
                    </div>
                    
                    <div class="donor-cards">
                        <div class="donor-card">
                            <div class="donor-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                            <div class="donor-info">
                                <h3 class="donor-name">Mumbere Darius</h3>
                                <div class="donor-contact">
                                    <span><i class="fas fa-envelope"></i> dariusmumbere@gmail.com</span>
                                    <span><i class="fas fa-phone"></i> +256 712 345 678</span>
                                </div>
                                <div class="donor-stats">
                                    <div class="stat-item">
                                        <span class="stat-label">Total Donations:</span>
                                        <span class="stat-value">UGX 2,500,000</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Last Donation:</span>
                                        <span class="stat-value">2023-10-15</span>
                                    </div>
                                </div>
                            </div>
                            <div class="donor-actions">
                                <button class="file-manager-btn secondary"><i class="fas fa-edit"></i> Edit</button>
                                <button class="file-manager-btn"><i class="fas fa-history"></i> View History</button>
                            </div>
                        </div>
                        
                        <div class="donor-card">
                            <div class="donor-avatar">
                                <i class="fas fa-building"></i>
                            </div>
                            <div class="donor-info">
                                <h3 class="donor-name">Acme Corp</h3>
                                <div class="donor-contact">
                                    <span><i class="fas fa-envelope"></i> contact@acme.com</span>
                                    <span><i class="fas fa-phone"></i> +256 312 345 678</span>
                                </div>
                                <div class="donor-stats">
                                    <div class="stat-item">
                                        <span class="stat-label">Total Donations:</span>
                                        <span class="stat-value">UGX 5,000,000</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Last Donation:</span>
                                        <span class="stat-value">2023-10-10</span>
                                    </div>
                                </div>
                            </div>
                            <div class="donor-actions">
                                <button class="file-manager-btn secondary"><i class="fas fa-edit"></i> Edit</button>
                                <button class="file-manager-btn"><i class="fas fa-history"></i> View History</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Add Donation Modal -->
                <div class="donation-modal" id="addDonationModal">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3>Add New Donation</h3>
                            <button class="close-btn" onclick="closeDonationModal()">&times;</button>
                        </div>
                        <div class="modal-body">
                            <form id="donationForm">
                                <div class="form-group">
                                    <label for="donorName">Donor Name</label>
                                    <input type="text" id="donorName" required>
                                </div>
                                <div class="form-group">
                                    <label for="donationAmount">Amount (UGX)</label>
                                    <input type="number" id="donationAmount" required>
                                </div>
                                <div class="form-group">
                                    <label for="paymentMethod">Payment Method</label>
                                    <select id="paymentMethod" required>
                                        <option value="">Select method</option>
                                        <option value="mobile_money">Mobile Money</option>
                                        <option value="bank_transfer">Bank Transfer</option>
                                        <option value="bank_transfer">Western Union</option>
                                        <option value="paypal">PayPal</option>
                                        <option value="cash">Cash</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="donationDate">Date</label>
                                    <input type="date" id="donationDate" required>
                                </div>
                                <div class="form-group">
                                    <label for="donationProject">Project/Campaign</label>
                                    <select id="donationProject">
                                        <option value="">General Donation</option>
                                        <option value="agriculture">Agriculture Extension</option>
                                        <option value="vocational">Vocational Education</option>
                                        <option value="women">Women Empowerment</option>
                                        <option value="economic">Economic Empowerment</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="donationNotes">Notes</label>
                                    <textarea id="donationNotes" rows="3"></textarea>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button class="file-manager-btn secondary" onclick="closeDonationModal()">Cancel</button>
                            <button class="file-manager-btn" onclick="submitDonation()">Save Donation</button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Add this modal to your HTML (place it with the other modals) -->
            <!-- Add this modal to your HTML (place it with the other modals) -->
<div class="donor-modal" id="donorModal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="donorModalTitle">Donor Profile</h3>
            <button class="close-btn" onclick="closeDonorModal()">&times;</button>
        </div>
        <div class="modal-body">
            <form id="donorForm">
                <input type="hidden" id="donorId">
                <div class="form-group">
                    <label for="donorName">Name*</label>
                    <input type="text" id="donorName" required>
                </div>
                <div class="form-group">
                    <label for="donorEmail">Email</label>
                    <input type="email" id="donorEmail">
                </div>
                <div class="form-group">
                    <label for="donorPhone">Phone</label>
                    <input type="tel" id="donorPhone">
                </div>
                <div class="form-group">
                    <label for="donorAddress">Address</label>
                    <textarea id="donorAddress" rows="2"></textarea>
                </div>
                <div class="form-group">
                    <label for="donorType">Donor Type</label>
                    <select id="donorType">
                        <option value="individual">Individual</option>
                        <option value="corporate">Corporate</option>
                        <option value="foundation">Foundation</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="donorCategory">Donor Category</label>
                    <select id="donorCategory">
                        <option value="one-time">One-time Donor</option>
                        <option value="regular">Regular Donor</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="donorNotes">Notes</label>
                    <textarea id="donorNotes" rows="3"></textarea>
                </div>
            </form>
            
            <div class="section-header" style="margin-top: 30px;">
                <h3 class="section-title">Donation History</h3>
            </div>
            <div class="table-responsive">
                <table class="donations-table" id="donorDonationsTable">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Amount</th>
                            <th>Project</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Donation history will be loaded here -->
                    </tbody>
                </table>
            </div>
            
            <div class="donor-stats" style="margin-top: 20px;">
                <div class="stat-item">
                    <span class="stat-label">Total Donations:</span>
                    <span class="stat-value" id="totalDonations">UGX 0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Donation Count:</span>
                    <span class="stat-value" id="donationCount">0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">First Donation:</span>
                    <span class="stat-value" id="firstDonation">-</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Last Donation:</span>
                    <span class="stat-value" id="lastDonation">-</span>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="file-manager-btn secondary" onclick="closeDonorModal()">Cancel</button>
            <button class="file-manager-btn" id="saveDonorBtn" type="button" onclick="document.getElementById('donorForm').dispatchEvent(new Event('submit'))">Save Donor</button>
        </div>
    </div>
</div>


            <!-- File Preview Modal -->
            <div class="file-preview-modal" id="filePreviewModal">
                <div class="file-preview-content">
                    <div class="file-preview-header">
                        <h3 id="previewFileName">File Preview</h3>
                        <button class="file-manager-btn secondary" onclick="closePreview()">
                            <i class="fas fa-times"></i> Close
                        </button>
                    </div>
                    <div class="file-preview-body" id="previewFileContent">
                        <!-- Content will be loaded here -->
                    </div>
                    <div class="file-preview-actions">
                        <button class="file-manager-btn" onclick="downloadCurrentFile()">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <button class="file-manager-btn secondary" onclick="closePreview()">
                            <i class="fas fa-times"></i> Close
                        </button>
                    </div>
                </div>
            </div>

            <!-- Create Folder Modal -->
            <div class="folder-create-modal" id="folderCreateModal">
                <div class="folder-create-content">
                    <div class="folder-create-header">
                        <h3>Create New Folder</h3>
                    </div>
                    <div class="folder-create-body">
                        <input type="text" class="folder-create-input" id="newFolderName" placeholder="Folder name">
                    </div>
                    <div class="folder-create-actions">
                        <button class="file-manager-btn secondary" onclick="closeCreateFolderModal()">
                            Cancel
                        </button>
                        <button class="file-manager-btn" onclick="createNewFolder()">
                            Create
                        </button>
                    </div>
                </div>
            </div>

            <!-- Upload Modal -->
            <div class="upload-modal" id="uploadModal">
                <div class="upload-content">
                    <div class="upload-header">
                        <h3>Upload Files</h3>
                    </div>
                    <div class="upload-area" id="uploadArea">
                        <i class="fas fa-cloud-upload-alt"></i>
                        <p>Drag & drop files here or <span class="browse-btn" id="browseFilesBtn">browse</span></p>
                        <p class="small">Supported formats: PDF, DOCX, XLSX, PPTX, JPG, PNG</p>
                        <input type="file" id="fileUploadInput" multiple>
                    </div>
                    <div class="upload-progress" id="uploadProgress">
                        <p>Uploading files...</p>
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill" id="progressBarFill"></div>
                        </div>
                    </div>
                    <div class="upload-actions">
                        <button class="file-manager-btn secondary" onclick="closeUploadModal()">
                            Cancel
                        </button>
                        <button class="file-manager-btn" id="startUploadBtn" disabled>
                            <i class="fas fa-upload"></i> Upload
                        </button>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const reportsMenu = document.getElementById('reportsMenu');
    const reportsSubmenu = document.getElementById('reportsSubmenu');
    const reportsArrow = document.getElementById('reportsArrow');
    const dashboardLink = document.getElementById('dashboardLink');
    const fundraisingLink = document.getElementById('fundraisingLink');
    const dashboardContent = document.getElementById('dashboardContent');
    const fileManagerContent = document.getElementById('fileManagerContent');
    const uploadFilesBtn = document.getElementById('uploadFilesBtn');
    const createFolderBtn = document.getElementById('createFolderBtn');
    const browseFilesBtn = document.getElementById('browseFilesBtn');
    const fileUploadInput = document.getElementById('fileUploadInput');
    const startUploadBtn = document.getElementById('startUploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBarFill = document.getElementById('progressBarFill');
    const donationsContent = document.getElementById('donationsContent');
    

    // Initialize with saved path or empty
    let currentPath = loadCurrentPath();
    let currentFileId = null;
    let currentFileName = null;
    let currentFileType = null;
    let filesToUpload = [];

    // Initialize by showing dashboard and hiding file manager
    dashboardContent.style.display = 'block';
    fileManagerContent.style.display = 'none';

    // Toggle sidebar collapse/expand
    menuToggle.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.toggle('show');
                } else {
                    sidebar.classList.toggle('collapsed');
                    
                    const icon = menuToggle.querySelector('i');
                    if (sidebar.classList.contains('collapsed')) {
                        icon.classList.remove('fa-bars');
                        icon.classList.add('fa-indent');
                    } else {
                        icon.classList.remove('fa-indent');
                        icon.classList.add('fa-bars');
                    }
                }
            });
            document.addEventListener('click', function(e) {
                if (window.innerWidth <= 768 && sidebar.classList.contains('show')) {
                    if (!e.target.closest('.sidebar') && !e.target.closest('.menu-toggle')) {
                        sidebar.classList.remove('show');
                    }
                }
            });

    // Toggle reports submenu
    reportsMenu.addEventListener('click', function(e) {
        e.preventDefault();
        reportsSubmenu.classList.toggle('show');
        reportsArrow.classList.toggle('fa-chevron-down');
        reportsArrow.classList.toggle('fa-chevron-up');
    });

    // Navigation between dashboard and file manager
    dashboardLink.addEventListener('click', function(e) {
        e.preventDefault();
        dashboardContent.style.display = 'block';
        fileManagerContent.style.display = 'none';
        setActiveNavItem(dashboardLink);
    });

    fundraisingLink.addEventListener('click', function(e) {
        e.preventDefault();
        dashboardContent.style.display = 'none';
        fileManagerContent.style.display = 'block';
        setActiveNavItem(fundraisingLink);
        
        // Load content for current path
        const folderId = currentPath.length > 0 ? currentPath[currentPath.length - 1].id : '';
        loadFolderContents(folderId);
    });

    // Initialize file manager
    initFileManager();

    // Check if we should show file manager based on URL hash
    if (window.location.hash === '#filemanager') {
        fundraisingLink.click();
    }

    function setActiveNavItem(activeItem) {
        const menuItems = document.querySelectorAll('.sidebar-menu li a');
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
        activeItem.classList.add('active');
    }

    // Save current path to localStorage
    function saveCurrentPath() {
        localStorage.setItem('currentPath', JSON.stringify(currentPath));
    }

    // Load current path from localStorage
    function loadCurrentPath() {
        const savedPath = localStorage.getItem('currentPath');
        return savedPath ? JSON.parse(savedPath) : [];
    }

    function initFileManager() {
        // Setup breadcrumb navigation
        setupBreadcrumb();

        // Setup create folder button
        createFolderBtn.addEventListener('click', openCreateFolderModal);

        // Setup upload files button
        uploadFilesBtn.addEventListener('click', openUploadModal);

        // Setup file upload handlers
        browseFilesBtn.addEventListener('click', () => fileUploadInput.click());
        fileUploadInput.addEventListener('change', handleFileSelection);
        startUploadBtn.addEventListener('click', startFileUpload);

        // Setup drag and drop for upload area
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'var(--primary-color)';
            uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#ccc';
            uploadArea.style.backgroundColor = 'transparent';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#ccc';
            uploadArea.style.backgroundColor = 'transparent';
            
            if (e.dataTransfer.files.length) {
                handleFileSelection({ target: { files: e.dataTransfer.files } });
            }
        });
    }

    function setupBreadcrumb() {
        const breadcrumb = document.getElementById('breadcrumb');
        breadcrumb.innerHTML = '';
        
        // Add root item
        const rootItem = document.createElement('span');
        rootItem.className = 'breadcrumb-item';
        rootItem.setAttribute('data-path', '');
        rootItem.textContent = 'Fundraising Documents';
        rootItem.addEventListener('click', () => navigateToFolder('', ''));
        breadcrumb.appendChild(rootItem);
        
        // Add current path items
        currentPath.forEach((folder, index) => {
            const separator = document.createElement('span');
            separator.className = 'breadcrumb-separator';
            separator.textContent = '›';
            breadcrumb.appendChild(separator);
            
            const item = document.createElement('span');
            item.className = 'breadcrumb-item';
            item.setAttribute('data-path', folder.id);
            item.textContent = folder.name;
            item.addEventListener('click', () => {
                // Navigate to this folder level
                const newPath = currentPath.slice(0, index + 1);
                navigateToPath(newPath);
            });
            breadcrumb.appendChild(item);
        });
    }

    async function navigateToFolder(folderId, folderName) {
        if (folderId) {
            currentPath.push({ id: folderId, name: folderName });
        } else {
            currentPath = [];
        }
        
        saveCurrentPath();
        setupBreadcrumb();
        await loadFolderContents(folderId);
    }

    function navigateToPath(path) {
        currentPath = path;
        saveCurrentPath();
        const folderId = path.length > 0 ? path[path.length - 1].id : '';
        loadFolderContents(folderId);
    }

    async function loadFolderContents(folderId) {
        try {
            // Show loading state
            const fileManagerGrid = document.getElementById('fileManagerGrid');
            fileManagerGrid.innerHTML = '<div class="loading">Loading contents...</div>';
            
            // Fetch folder contents from backend
            const response = await fetch(`https://man-m681.onrender.com/folders/${folderId || 'root'}/contents`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch folder contents');
            }
            
            const data = await response.json();
            
            // Clear the grid
            fileManagerGrid.innerHTML = '';
            
            // Add folders
            data.folders.forEach(folder => {
                const folderItem = createFolderElement(folder.id, folder.name);
                fileManagerGrid.appendChild(folderItem);
            });
            
            // Add files
            data.files.forEach(file => {
                const fileItem = createFileElement(file.id, file.name, file.type);
                fileManagerGrid.appendChild(fileItem);
            });
            
        } catch (error) {
            console.error('Error loading folder contents:', error);
            alert('Failed to load folder contents. Please try again.');
        }
    }

    function createFolderElement(folderId, folderName) {
        const folderItem = document.createElement('div');
        folderItem.className = 'folder-item';
        folderItem.setAttribute('data-folder-id', folderId);
        folderItem.setAttribute('data-folder-name', folderName);
        folderItem.innerHTML = `
            <div class="folder-icon">
                <i class="fas fa-folder"></i>
            </div>
            <div class="folder-name">${folderName}</div>
            <div class="file-actions-menu" onclick="event.stopPropagation(); toggleFolderActions(event, '${folderId}')">
                <i class="fas fa-ellipsis-v"></i>
            </div>
            <div class="file-actions-dropdown" id="folder-actions-${folderId}">
                <div class="file-action-item" onclick="renameFolder('${folderId}', '${folderName}')">
                    <i class="fas fa-pencil-alt"></i> Rename
                </div>
                <div class="file-action-item" onclick="deleteFolder('${folderId}')">
                    <i class="fas fa-trash"></i> Delete
                </div>
            </div>
        `;
        
        folderItem.addEventListener('click', function(e) {
            if (!e.target.closest('.file-actions-menu') && !e.target.closest('.file-actions-dropdown')) {
                navigateToFolder(folderId, folderName);
            }
        });
        
        return folderItem;
    }

    function createFileElement(fileId, fileName, fileType) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.setAttribute('data-file-id', fileId);
        fileItem.setAttribute('data-file-name', fileName);
        fileItem.innerHTML = `
            <div class="file-icon">
                <i class="fas ${getFileIcon(fileType)}"></i>
            </div>
            <div class="file-name">${fileName}</div>
            <div class="file-actions-menu" onclick="event.stopPropagation(); toggleFileActions(event, '${fileId}')">
                <i class="fas fa-ellipsis-v"></i>
            </div>
            <div class="file-actions-dropdown" id="file-actions-${fileId}">
                <div class="file-action-item" onclick="previewFile('${fileId}', '${fileName}', '${fileType}')">
                    <i class="fas fa-eye"></i> Preview
                </div>
                <div class="file-action-item" onclick="downloadFile('${fileId}', '${fileName}')">
                    <i class="fas fa-download"></i> Download
                </div>
                <div class="file-action-item" onclick="renameFile('${fileId}', '${fileName}')">
                    <i class="fas fa-pencil-alt"></i> Rename
                </div>
                <div class="file-action-item" onclick="deleteFile('${fileId}', '${fileName}')">
                    <i class="fas fa-trash"></i> Delete
                </div>
            </div>
        `;
        return fileItem;
    }

    function toggleFileActions(event, fileId) {
        event.stopPropagation();
        const dropdown = document.getElementById(`file-actions-${fileId}`);
        document.querySelectorAll('.file-actions-dropdown').forEach(d => {
            if (d !== dropdown) d.classList.remove('show');
        });
        dropdown.classList.toggle('show');
    }

    function toggleFolderActions(event, folderId) {
        event.stopPropagation();
        const dropdown = document.getElementById(`folder-actions-${folderId}`);
        document.querySelectorAll('.file-actions-dropdown').forEach(d => {
            if (d !== dropdown) d.classList.remove('show');
        });
        dropdown.classList.toggle('show');
    }

    function previewFile(fileId, fileName, fileType) {
        currentFileId = fileId;
        currentFileName = fileName;
        currentFileType = fileType;
        
        document.getElementById('previewFileName').textContent = fileName;
        const previewContent = document.getElementById('previewFileContent');
        previewContent.innerHTML = '';
        
        // Create appropriate preview based on file type
        if (fileType === 'pdf') {
            const iframe = document.createElement('iframe');
            iframe.className = 'file-preview-iframe';
            iframe.src = `https://man-m681.onrender.com/files/${fileId}/preview`;
            previewContent.appendChild(iframe);
        } else if (['jpg', 'jpeg', 'png', 'gif'].includes(fileType)) {
            const img = document.createElement('img');
            img.className = 'file-preview-image';
            img.src = `https://man-m681.onrender.com/files/${fileId}/preview`;
            img.alt = fileName;
            previewContent.appendChild(img);
        } else {
            // For unsupported preview types, show a message
            const message = document.createElement('div');
            message.textContent = 'Preview not available for this file type. Please download to view.';
            previewContent.appendChild(message);
        }
        
        document.getElementById('filePreviewModal').classList.add('show');
    }

    function closePreview() {
        document.getElementById('filePreviewModal').classList.remove('show');
    }

    function downloadCurrentFile() {
        downloadFile(currentFileId, currentFileName);
        closePreview();
    }

    async function downloadFile(fileId, fileName) {
        try {
            // Show loading state
            const originalText = startUploadBtn.innerHTML;
            startUploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
            startUploadBtn.disabled = true;
            
            window.location.href = `https://man-m681.onrender.com/files/${fileId}/download`;
        } catch (error) {
            console.error('Error downloading file:', error);
            alert('Failed to download file. Please try again.');
        } finally {
            startUploadBtn.innerHTML = 'Upload';
            startUploadBtn.disabled = false;
        }
    }

    async function renameFile(fileId, currentName) {
        const newName = prompt('Enter new file name:', currentName);
        if (newName && newName !== currentName) {
            try {
                const response = await fetch(`https://man-m681.onrender.com/files/${fileId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: newName
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to rename file');
                }
                
                // Update the UI
                const fileItem = document.querySelector(`.file-item[data-file-id="${fileId}"]`);
                if (fileItem) {
                    fileItem.setAttribute('data-file-name', newName);
                    fileItem.querySelector('.file-name').textContent = newName;
                }
            } catch (error) {
                console.error('Error renaming file:', error);
                alert('Failed to rename file. Please try again.');
            }
        }
    }

    async function deleteFile(fileId, fileName) {
        if (confirm(`Are you sure you want to delete "${fileName}"?`)) {
            try {
                const response = await fetch(`https://man-m681.onrender.com/files/${fileId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) {
                    throw new Error('Failed to delete file');
                }
                
                // Remove from UI
                const fileItem = document.querySelector(`.file-item[data-file-id="${fileId}"]`);
                if (fileItem) {
                    fileItem.remove();
                }
            } catch (error) {
                console.error('Error deleting file:', error);
                alert('Failed to delete file. Please try again.');
            }
        }
    }

    function openCreateFolderModal() {
        document.getElementById('newFolderName').value = '';
        document.getElementById('folderCreateModal').classList.add('show');
    }

    function closeCreateFolderModal() {
        document.getElementById('folderCreateModal').classList.remove('show');
    }

    async function createNewFolder() {
        const folderName = document.getElementById('newFolderName').value.trim();
        if (!folderName) {
            alert('Please enter a folder name');
            return;
        }
        
        try {
            const currentFolderId = currentPath.length > 0 ? currentPath[currentPath.length - 1].id : '';
            
            const formData = new FormData();
            formData.append('name', folderName);
            if (currentFolderId) {
                formData.append('parent_id', currentFolderId);
            }
            
            const response = await fetch('https://man-m681.onrender.com/folders/', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to create folder');
            }
            
            const data = await response.json();
            
            // Add the new folder to the UI
            const folderItem = createFolderElement(data.id, folderName);
            document.getElementById('fileManagerGrid').prepend(folderItem);
            
            closeCreateFolderModal();
        } catch (error) {
            console.error('Error creating folder:', error);
            alert('Failed to create folder. Please try again.');
        }
    }

    async function renameFolder(folderId, currentName) {
        const newName = prompt('Enter new folder name:', currentName);
        if (newName && newName !== currentName) {
            try {
                const response = await fetch(`https://man-m681.onrender.com/folders/${folderId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: newName
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to rename folder');
                }
                
                // Update the UI
                const folderItem = document.querySelector(`.folder-item[data-folder-id="${folderId}"]`);
                if (folderItem) {
                    folderItem.setAttribute('data-folder-name', newName);
                    folderItem.querySelector('.folder-name').textContent = newName;
                    
                    // Update in currentPath if needed
                    currentPath = currentPath.map(folder => {
                        if (folder.id === folderId) {
                            return { ...folder, name: newName };
                        }
                        return folder;
                    });
                    
                    // Update breadcrumb if needed
                    setupBreadcrumb();
                }
            } catch (error) {
                console.error('Error renaming folder:', error);
                alert('Failed to rename folder. Please try again.');
            }
        }
    }

    async function deleteFolder(folderId) {
        const folderItem = document.querySelector(`.folder-item[data-folder-id="${folderId}"]`);
        const folderName = folderItem ? folderItem.getAttribute('data-folder-name') : '';
        
        if (confirm(`Are you sure you want to delete the folder "${folderName}" and all its contents?`)) {
            try {
                const response = await fetch(`https://man-m681.onrender.com/folders/${folderId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) {
                    throw new Error('Failed to delete folder');
                }
                
                // Remove from UI
                if (folderItem) {
                    folderItem.remove();
                }
            } catch (error) {
                console.error('Error deleting folder:', error);
                alert('Failed to delete folder. Please try again.');
            }
        }
    }

    function openUploadModal() {
        filesToUpload = [];
        fileUploadInput.value = '';
        startUploadBtn.disabled = true;
        uploadProgress.style.display = 'none';
        document.getElementById('uploadModal').classList.add('show');
    }

    function closeUploadModal() {
        document.getElementById('uploadModal').classList.remove('show');
    }

    function handleFileSelection(event) {
        filesToUpload = Array.from(event.target.files);
        if (filesToUpload.length > 0) {
            startUploadBtn.disabled = false;
            // Show selected files count
            document.querySelector('#uploadArea p').textContent = `${filesToUpload.length} file(s) selected for upload`;
        }
    }

    async function startFileUpload() {
        if (filesToUpload.length === 0) return;
        
        uploadProgress.style.display = 'block';
        startUploadBtn.disabled = true;
        const originalText = startUploadBtn.innerHTML;
        startUploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        
        try {
            const currentFolderId = currentPath.length > 0 ? currentPath[currentPath.length - 1].id : '';
            const formData = new FormData();
            
            // Add all files to FormData
            for (let i = 0; i < filesToUpload.length; i++) {
                formData.append('files', filesToUpload[i]);
            }
            
            // Add folder ID if we're in a subfolder
            if (currentFolderId) {
                formData.append('folder_id', currentFolderId);
            }
            
            const response = await fetch('https://man-m681.onrender.com/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('File upload failed');
            }
            
            const data = await response.json();
            
            // Add uploaded files to UI
            data.uploadedFiles.forEach(file => {
                const fileItem = createFileElement(file.id, file.name, file.type);
                document.getElementById('fileManagerGrid').appendChild(fileItem);
            });
            
            alert('Files uploaded successfully!');
            closeUploadModal();
        } catch (error) {
            console.error('Error uploading files:', error);
            alert('Failed to upload files. Please try again.');
        } finally {
            progressBarFill.style.width = '0%';
            startUploadBtn.innerHTML = originalText;
            startUploadBtn.disabled = false;
        }
    }

    function getFileIcon(fileType) {
        switch(fileType) {
            case 'pdf': return 'fa-file-pdf';
            case 'doc':
            case 'docx': return 'fa-file-word';
            case 'xls':
            case 'xlsx': return 'fa-file-excel';
            case 'ppt':
            case 'pptx': return 'fa-file-powerpoint';
            case 'jpg':
            case 'jpeg':
            case 'png':
            case 'gif': return 'fa-file-image';
            default: return 'fa-file';
        }
    }

    // Close dropdowns when clicking elsewhere
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.file-actions-menu') && !e.target.closest('.file-actions-dropdown')) {
            document.querySelectorAll('.file-actions-dropdown').forEach(d => {
                d.classList.remove('show');
            });
        }
    });

    // Expose functions to global scope for inline event handlers
    window.toggleFileActions = toggleFileActions;
    window.toggleFolderActions = toggleFolderActions;
    window.previewFile = previewFile;
    window.downloadFile = downloadFile;
    window.renameFile = renameFile;
    window.deleteFile = deleteFile;
    window.renameFolder = renameFolder;
    window.deleteFolder = deleteFolder;
    window.closePreview = closePreview;
    window.downloadCurrentFile = downloadCurrentFile;
    window.closeCreateFolderModal = closeCreateFolderModal;
    window.createNewFolder = createNewFolder;
});
                // Donations Page Functionality
        const donationsLink = document.getElementById('donationsLink');
        const donationsContent = document.getElementById('donationsContent');
        const tabBtns = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        const addDonationBtn = document.getElementById('addDonationBtn');
        const addDonationModal = document.getElementById('addDonationModal');

        // Navigation to donations page
        donationsLink.addEventListener('click', function(e) {
    e.preventDefault();
    dashboardContent.style.display = 'none';
    fileManagerContent.style.display = 'none';
    donationsContent.style.display = 'block';
    setActiveNavItem(donationsLink);
});

        // Tab switching
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all buttons and contents
                tabBtns.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked button and corresponding content
                this.classList.add('active');
                const tabId = this.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });

        // Add donation modal
        addDonationBtn.addEventListener('click', function() {
            addDonationModal.classList.add('show');
        });

        function closeDonationModal() {
            addDonationModal.classList.remove('show');
        }

        function submitDonation() {
            // Here you would normally send the data to your backend
            alert('Donation submitted successfully!');
            closeDonationModal();
            // Reset form
            document.getElementById('donationForm').reset();
        }

        // Close modal when clicking outside
        window.addEventListener('click', function(e) {
            if (e.target === addDonationModal) {
                closeDonationModal();
            }
        });

        // Expose functions to global scope
        window.closeDonationModal = closeDonationModal;
        window.submitDonation = submitDonation;

        async function submitDonation() {
    const donorName = document.getElementById('donorName').value;
    const donationAmount = parseFloat(document.getElementById('donationAmount').value);
    const paymentMethod = document.getElementById('paymentMethod').value;
    const donationDate = document.getElementById('donationDate').value;
    const donationProject = document.getElementById('donationProject').value;
    const donationNotes = document.getElementById('donationNotes').value;

    if (!donorName || !donationAmount || !paymentMethod || !donationDate) {
        alert('Please fill in all required fields');
        return;
    }

    try {
        const response = await fetch('https://man-m681.onrender.com/donations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                donor_name: donorName,
                amount: donationAmount,
                payment_method: paymentMethod, 
                date: donationDate,
                project: donationProject,
                notes: donationNotes
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit donation');
        }

        const data = await response.json();
        alert('Donation submitted successfully!');
        
        // Close the modal and refresh the donations table
        closeDonationModal();
        loadDonations();
        
        // Reset form
        document.getElementById('donationForm').reset();
    } catch (error) {
        console.error('Error submitting donation:', error);
        alert('Failed to submit donation. Please try again.');
    }
}

// Add this function to load donations
async function loadDonations() {
    try {
        const donationsTable = document.querySelector('.donations-table tbody');
        donationsTable.innerHTML = '<tr><td colspan="7" style="text-align: center;">Loading donations...</td></tr>';
        
        const response = await fetch('https://man-m681.onrender.com/donations/');
        
        if (!response.ok) {
            throw new Error('Failed to fetch donations');
        }
        
        const data = await response.json();
        donationsTable.innerHTML = '';
        
        data.donations.forEach(donation => {
            // Extract payment method from the purpose field or use default
            let paymentMethod = 'Not specified';
            if (donation.purpose) {
                // This assumes payment method is stored in the purpose field
                // You might need to adjust this based on your actual data structure
                if (donation.purpose.includes('Mobile Money')) paymentMethod = 'Mobile Money';
                else if (donation.purpose.includes('Bank Transfer')) paymentMethod = 'Bank Transfer';
                else if (donation.purpose.includes('PayPal')) paymentMethod = 'PayPal';
                else if (donation.purpose.includes('Cash')) paymentMethod = 'Cash';
            }
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${donation.date}</td>
                <td>${donation.donor_name}</td>
                <td>UGX ${donation.amount.toLocaleString()}</td>
                <td>${paymentMethod}</td>
                <td>${donation.project || 'General Fund'}</td>
                <td><span class="status-badge completed">Completed</span></td>
                <td>
                    <button class="action-btn view-btn"><i class="fas fa-eye"></i></button>
                    <button class="action-btn edit-btn"><i class="fas fa-edit"></i></button>
                    <button class="action-btn delete-btn"><i class="fas fa-trash"></i></button>
                </td>
            `;
            donationsTable.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading donations:', error);
        donationsTable.innerHTML = '<tr><td colspan="7" style="text-align: center; color: red;">Failed to load donations</td></tr>';
    }
}
// Add these functions for CRUD operations
async function viewDonation(donationId) {
    // Implement view functionality
    alert(`View donation ${donationId}`);
}

async function editDonation(donationId) {
    // Implement edit functionality
    alert(`Edit donation ${donationId}`);
}

async function deleteDonation(donationId) {
    if (confirm('Are you sure you want to delete this donation record?')) {
        try {
            const response = await fetch(`https://man-m681.onrender.com/donations/${donationId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete donation');
            }
            
            alert('Donation deleted successfully');
            loadDonations();
        } catch (error) {
            console.error('Error deleting donation:', error);
            alert('Failed to delete donation. Please try again.');
        }
    }
}
        // Tab switching functionality
function setupTabSwitching() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');

            // Load content for the active tab
            switch(tabId) {
                case 'donationHistory':
                    loadDonations();
                    break;
                case 'receipts':
                    // You can add a loadReceipts() function later
                    break;
                case 'donorProfiles':
                    // You can add a loadDonorProfiles() function later
                    break;
            }
        });
    });
}

// Call this function when the donations content is shown
// Update your showDonationsContent function
function showDonationsContent() {
    dashboardContent.style.display = 'none';
    fileManagerContent.style.display = 'none';
    donationsContent.style.display = 'block';
    setActiveNavItem(donationsLink);
    
    // Always load donations when showing this content
    loadDonations();
    
    // Set the first tab as active
    const firstTabBtn = document.querySelector('.donations-tabs .tab-btn');
    firstTabBtn.classList.add('active');
    document.getElementById('donationHistory').classList.add('active');
}

// Update your DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    setupTabSwitching();
    
    // Check if we're on the donations page (either by default or via URL hash)
    if (window.location.hash === '#donations' || donationsContent.style.display === 'block') {
        showDonationsContent();
    }
});

// Initialize tab switching when the page loads
document.addEventListener('DOMContentLoaded', function() {
    setupTabSwitching();
    
    // If donations content is shown by default (e.g., from URL hash)
    if (window.location.hash === '#donations') {
        showDonationsContent();
    }
});
        window.submitDonation = submitDonation;
window.viewDonation = viewDonation;
window.editDonation = editDonation;
window.deleteDonation = deleteDonation;

        // Add these to your existing JavaScript

// Global variable to track current donor
let currentDonorId = null;

// Function to open donor modal
function openDonorModal(donorId = null) {
    currentDonorId = donorId;
    const modal = document.getElementById('donorModal');
    const title = document.getElementById('donorModalTitle');
    const saveBtn = document.getElementById('saveDonorBtn');
    
    if (donorId) {
        title.textContent = 'Edit Donor Profile';
        saveBtn.textContent = 'Update Donor';
        loadDonorData(donorId);
    } else {
        title.textContent = 'Add New Donor';
        saveBtn.textContent = 'Add Donor';
        document.getElementById('donorForm').reset();
        document.getElementById('donorDonationsTable').querySelector('tbody').innerHTML = 
            '<tr><td colspan="4" style="text-align: center;">No donation history available</td></tr>';
        document.getElementById('totalDonations').textContent = 'UGX 0';
        document.getElementById('donationCount').textContent = '0';
        document.getElementById('firstDonation').textContent = '-';
        document.getElementById('lastDonation').textContent = '-';
    }
    
    modal.classList.add('show');
}


// Function to close donor modal
function closeDonorModal() {
    document.getElementById('donorModal').classList.remove('show');
    currentDonorId = null;
}

// Function to load donor data
async function loadDonorData(donorId) {
    try {
        const response = await fetch(`https://man-m681.onrender.com/donors/${donorId}`);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch donor data');
        }
        
        const donor = await response.json();
        
        // Populate form
        document.getElementById('donorId').value = donor.id;
        document.getElementById('donorName').value = donor.name;
        document.getElementById('donorEmail').value = donor.email || '';
        document.getElementById('donorPhone').value = donor.phone || '';
        document.getElementById('donorAddress').value = donor.address || '';
        document.getElementById('donorType').value = donor.donor_type || 'individual';
        document.getElementById('donorCategory').value = donor.category || 'one-time';
        document.getElementById('donorNotes').value = donor.notes || '';
        
        // Load donation history
        loadDonorDonations(donorId);
    } catch (error) {
        console.error('Error loading donor data:', error);
        alert(`Failed to load donor data: ${error.message}`);
    }
}

// Function to load donor's donations
async function loadDonorDonations(donorId) {
    try {
        const response = await fetch(`https://man-m681.onrender.com/donors/${donorId}/donations`);
        if (!response.ok) throw new Error('Failed to fetch donor donations');
        
        const data = await response.json();
        const tbody = document.getElementById('donorDonationsTable').querySelector('tbody');
        tbody.innerHTML = '';
        
        if (data.donations.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No donation history available</td></tr>';
        } else {
            data.donations.forEach(donation => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donation.date}</td>
                    <td>UGX ${donation.amount.toLocaleString()}</td>
                    <td>${donation.project}</td>
                    <td><span class="status-badge completed">${donation.status}</span></td>
                `;
                tbody.appendChild(row);
            });
        }
        
        // Update stats
        document.getElementById('totalDonations').textContent = `UGX ${data.total_donations.toLocaleString()}`;
        document.getElementById('donationCount').textContent = data.donation_count;
        
        if (data.donations.length > 0) {
            const dates = data.donations.map(d => new Date(d.date));
            dates.sort((a, b) => a - b);
            document.getElementById('firstDonation').textContent = dates[0].toLocaleDateString();
            document.getElementById('lastDonation').textContent = dates[dates.length - 1].toLocaleDateString();
        } else {
            document.getElementById('firstDonation').textContent = '-';
            document.getElementById('lastDonation').textContent = '-';
        }
    } catch (error) {
        console.error('Error loading donor donations:', error);
        alert('Failed to load donation history. Please try again.');
    }
}

// Function to save donor
async function saveDonor() {
    // Validate form before proceeding
    if (!validateDonorForm()) {
        return;
    }
    
    // Get form data
    const donorData = {
        name: document.getElementById('donorName').value.trim(),
        email: document.getElementById('donorEmail').value.trim(),
        phone: document.getElementById('donorPhone').value.trim(),
        address: document.getElementById('donorAddress').value.trim(),
        donor_type: document.getElementById('donorType').value,
        category: document.getElementById('donorCategory').value,
        notes: document.getElementById('donorNotes').value.trim()
    };
    
    try {
        const isEdit = !!currentDonorId;
        const url = isEdit 
            ? `https://man-m681.onrender.com/donors/${currentDonorId}`
            : 'https://man-m681.onrender.com/donors/';
        const method = isEdit ? 'PUT' : 'POST';
        
        // Show loading state
        const saveBtn = document.getElementById('saveDonorBtn');
        const originalText = saveBtn.innerHTML;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        saveBtn.disabled = true;
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(donorData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to save donor');
        }
        
        // Success - reload donor list and close modal
        await loadDonorProfiles();
        closeDonorModal();
        
    } catch (error) {
        console.error('Save donor error:', error);
        alert(`Error: ${error.message}`);
    } finally {
        // Restore button state
        const saveBtn = document.getElementById('saveDonorBtn');
        saveBtn.innerHTML = currentDonorId ? 'Update Donor' : 'Add Donor';
        saveBtn.disabled = false;
    }
}
        function validateDonorForm() {
    const nameInput = document.getElementById('donorName');
    const donorName = nameInput.value.trim();
    
    if (!donorName) {
        alert('Please enter donor name');
        nameInput.focus();
        return false;
    }
    
    // Additional validations can be added here if needed
    return true;
}


// Add event listener in your DOMContentLoaded
document.getElementById('donorForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveDonor();
});

// Update your save button to trigger form submission
document.getElementById('saveDonorBtn').addEventListener('click', function() {
    document.getElementById('donorForm').dispatchEvent(new Event('submit'));
});
        
// Function to load donor profiles
async function loadDonorProfiles(search = '') {
    try {
        const response = await fetch(`https://man-m681.onrender.com/donors/?search=${encodeURIComponent(search)}`);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch donors');
        }
        
        const donors = await response.json();
        const container = document.querySelector('.donor-cards');
        container.innerHTML = '';
        
        if (donors.length === 0) {
            container.innerHTML = '<p>No donors found. Add a new donor to get started.</p>';
            return;
        }
        
        donors.forEach(donor => {
            const donorCard = document.createElement('div');
            donorCard.className = 'donor-card';
            donorCard.innerHTML = `
                <div class="donor-avatar">
                    <i class="fas ${donor.donor_type === 'corporate' ? 'fa-building' : 'fa-user'}"></i>
                </div>
                <div class="donor-info">
                    <h3 class="donor-name">${donor.name}</h3>
                    <div class="donor-contact">
                        ${donor.email ? `<span><i class="fas fa-envelope"></i> ${donor.email}</span>` : ''}
                        ${donor.phone ? `<span><i class="fas fa-phone"></i> ${donor.phone}</span>` : ''}
                    </div>
                    <div class="donor-stats">
                        <div class="stat-item">
                            <span class="stat-label">Type:</span>
                            <span class="stat-value">${donor.donor_type || 'Not specified'}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Category:</span>
                            <span class="stat-value">${donor.category || 'Not specified'}</span>
                        </div>
                    </div>
                </div>
                <div class="donor-actions">
                    <button class="file-manager-btn secondary" onclick="openDonorModal(${donor.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="file-manager-btn" onclick="viewDonorHistory(${donor.id})">
                        <i class="fas fa-history"></i> View History
                    </button>
                </div>
            `;
            container.appendChild(donorCard);
        });
    } catch (error) {
        console.error('Error loading donors:', error);
        alert(`Failed to load donors: ${error.message}`);
    }
}


// Function to view donor history (opens modal with donations)
function viewDonorHistory(donorId) {
    currentDonorId = donorId;
    openDonorModal(donorId);
}

// Function to delete donor
async function deleteDonor(donorId) {
    if (!confirm('Are you sure you want to delete this donor? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`https://man-m681.onrender.com/donors/${donorId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete donor');
        
        alert('Donor deleted successfully');
        loadDonorProfiles();
    } catch (error) {
        console.error('Error deleting donor:', error);
        alert('Failed to delete donor. Please try again.');
    }
}

// Initialize donor functionality when donations tab is shown
function showDonationsContent() {
    dashboardContent.style.display = 'none';
    fileManagerContent.style.display = 'none';
    donationsContent.style.display = 'block';
    setActiveNavItem(donationsLink);
    
    // Load donations when showing this content
    loadDonations();
    
    // Set the first tab as active
    const firstTabBtn = document.querySelector('.donations-tabs .tab-btn');
    firstTabBtn.classList.add('active');
    document.getElementById('donationHistory').classList.add('active');
    
    // Load donor profiles if on donor tab
    if (document.getElementById('donorProfiles').classList.contains('active')) {
        loadDonorProfiles();
    }
}

// Update tab switching to load appropriate content
function setupTabSwitching() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');

            // Load content for the active tab
            switch(tabId) {
                case 'donationHistory':
                    loadDonations();
                    break;
                case 'receipts':
                    // You can add a loadReceipts() function later
                    break;
                case 'donorProfiles':
                    loadDonorProfiles();
                    break;
            }
        });
    });
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add donor button
    document.getElementById('addDonorBtn').addEventListener('click', function() {
        openDonorModal();
    });
    
    // Save donor form submission
    document.getElementById('donorForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveDonor();
    });
    
    // Initialize tab switching
    setupTabSwitching();
    
    // Load donor profiles if on donor tab
    if (document.getElementById('donorProfiles').classList.contains('active')) {
        loadDonorProfiles();
    }
});

// Expose functions to global scope
window.openDonorModal = openDonorModal;
window.closeDonorModal = closeDonorModal;
window.viewDonorHistory = viewDonorHistory;
window.saveDonor = saveDonor;
window.deleteDonor = deleteDonor       
    </script>
</body>
</html>
