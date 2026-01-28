// Simple JavaScript for Mega Menu
    document.addEventListener('DOMContentLoaded', function() {
        const megaMenuToggles = document.querySelectorAll('.mega-menu .dropdown-toggle');
        
        megaMenuToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth < 992) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Close other open menus
                    document.querySelectorAll('.mega-menu').forEach(menu => {
                        if (menu !== this.parentElement) {
                            menu.classList.remove('show');
                        }
                    });
                    
                    // Toggle current menu
                    const megaMenu = this.parentElement;
                    megaMenu.classList.toggle('show');
                }
            });
        });
        
        // Close mega menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.mega-menu')) {
                document.querySelectorAll('.mega-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
        
        // Close mega menu on mobile scroll
        window.addEventListener('scroll', function() {
            if (window.innerWidth < 992) {
                document.querySelectorAll('.mega-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
        
        // Simple hover effect for menu items
        const menuItems = document.querySelectorAll('.menu-list .dropdown-item');
        menuItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.15s ease';
            });
        });
        
        // Auto-adjust menu list heights based on content
        function adjustMenuHeights() {
            const menuLists = document.querySelectorAll('.menu-list');
            menuLists.forEach(list => {
                const items = list.querySelectorAll('li');
                const itemCount = items.length;
                
                if (itemCount > 7) {
                    list.style.maxHeight = '250px';
                    list.style.overflowY = 'auto';
                } else {
                    list.style.maxHeight = 'none';
                    list.style.overflowY = 'visible';
                }
            });
        }
        
        // Initialize
        adjustMenuHeights();
        
        // Re-adjust on window resize
        window.addEventListener('resize', adjustMenuHeights);
        
        // اسکریپت جدید برای تغییر رنگ هنگام اسکرول
        const navbar = document.querySelector('.navbar');
        const threshold = 100;
        
        function handleScroll() {
            if (window.scrollY > threshold) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
        
        window.addEventListener('scroll', handleScroll);
        
        if (window.scrollY > threshold) {
            navbar.classList.add('scrolled');
        }
        
        // مدیریت منوهای آیکون‌ها برای دسکتاپ
        if (window.innerWidth >= 992) {
            const iconContainers = document.querySelectorAll('.header_icon_container');
            
            iconContainers.forEach(container => {
                const dropdownMenu = container.querySelector('.dropdown-menu');
                
                container.addEventListener('mouseenter', function() {
                    if (dropdownMenu) {
                        dropdownMenu.style.display = 'block';
                        dropdownMenu.style.opacity = '0';
                        dropdownMenu.style.transform = 'translateY(10px)';
                        
                        setTimeout(() => {
                            dropdownMenu.style.opacity = '1';
                            dropdownMenu.style.transform = 'translateY(0)';
                            dropdownMenu.style.transition = 'all 0.3s ease';
                        }, 10);
                    }
                });
                
                container.addEventListener('mouseleave', function(e) {
                    if (dropdownMenu && !container.contains(e.relatedTarget)) {
                        dropdownMenu.style.opacity = '0';
                        dropdownMenu.style.transform = 'translateY(10px)';
                        
                        setTimeout(() => {
                            dropdownMenu.style.display = 'none';
                        }, 300);
                    }
                });
            });
        }
    });

    function changeLanguage(lang) {
        document.getElementById('lang-code').value = lang;
        document.getElementById('lang-form').submit();
    }

    // Language Change Function - Keep only one version
    function changeLanguage(lang) {
        const form = document.getElementById('lang-form');
        const langInput = document.getElementById('lang-code');
        
        // Set selected language
        langInput.value = lang;
        
        // Optional: Add loading indicator
        const currentLang = document.querySelector('.current-language');
        if (currentLang) {
            currentLang.style.opacity = '0.7';
        }
        
        // Submit form
        form.submit();
    }

    // Set default language to Turkish on page load if not set
    document.addEventListener('DOMContentLoaded', function() {
        const currentLang = "{{ CURRENT_LANG|default:'tr' }}";
        
        // If language is not set, default to Turkish
        if (!currentLang || currentLang === 'None') {
            const langForm = document.getElementById('lang-form');
            const langInput = document.getElementById('lang-code');
            
            if (langForm && langInput) {
                // Don't auto-submit, just update UI
                const currentLangDisplay = document.querySelector('.language-code');
                const currentFlag = document.querySelector('.language-flag .flag-icon');
                
                if (currentLangDisplay) {
                    currentLangDisplay.textContent = 'TR';
                }
                
                if (currentFlag) {
                    currentFlag.className = 'flag-icon flag-icon-tr';
                }
            }
        }
    });

    // Function to get current language from cookie
    function getCurrentLanguage() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('django_language='))
            ?.split('=')[1];
        
        return cookieValue || 'tr'; // Default to Turkish
    }

    // Update UI based on cookie language
    function updateLanguageFromCookie() {
        const lang = getCurrentLanguage();
        const currentLangDisplay = document.querySelector('.language-code');
        const currentFlag = document.querySelector('.language-flag .flag-icon');
        
        if (!currentLangDisplay || !currentFlag) return;
        
        // Update flag and code
        currentFlag.className = 'flag-icon';
        switch(lang) {
            case 'tr':
                currentFlag.classList.add('flag-icon-tr');
                currentLangDisplay.textContent = 'TR';
                break;
            case 'en':
                currentFlag.classList.add('flag-icon-gb');
                currentLangDisplay.textContent = 'EN';
                break;
            case 'fa':
                currentFlag.classList.add('flag-icon-ir');
                currentLangDisplay.textContent = 'FA';
                break;
            case 'ar':
                currentFlag.classList.add('flag-icon-sa');
                currentLangDisplay.textContent = 'AR';
                break;
            case 'ru':
                currentFlag.classList.add('flag-icon-ru');
                currentLangDisplay.textContent = 'RU';
                break;
            case 'de':
                currentFlag.classList.add('flag-icon-de');
                currentLangDisplay.textContent = 'DE';
                break;
            default:
                currentFlag.classList.add('flag-icon-tr');
                currentLangDisplay.textContent = 'TR';
        }
        
        // Update active items in dropdown
        document.querySelectorAll('.language-dropdown .dropdown-item').forEach(item => {
            item.classList.remove('active-language');
            item.querySelector('.text-primary')?.remove();
            
            // Check if this item matches current language
            const onclickAttr = item.getAttribute('onclick');
            if (onclickAttr && onclickAttr.includes(`'${lang}'`)) {
                item.classList.add('active-language');
                const checkmark = document.createElement('span');
                checkmark.className = 'ms-auto text-primary';
                checkmark.innerHTML = '✓';
                item.appendChild(checkmark);
            }
        });
    }

    // Call this on page load
    document.addEventListener('DOMContentLoaded', function() {
        updateLanguageFromCookie();
        
        // Also update when language changes (for AJAX solution)
        window.addEventListener('languageChanged', updateLanguageFromCookie);
    });