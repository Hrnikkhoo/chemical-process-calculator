// تنظیمات اولیه پارامترهای محاسباتی
const params = {
    sas: 0.682,     // ضریب شیرینی
    sv: 0.63,        // ضریب الکل
    cts: 1.11,       // ضریب تبدیل
    kss: 0.025,      // پارامتر تخصصی 1
    kss_w: 0.05,     // پارامتر تخصصی 2
    pas: 0.78927,    // چگالی الکل
    kip: 78.37,      // نقطه جوش
    t_w: 4.2         // دمای آب
};

// تعریف هسته اصلی ماشین حساب
$.prototype.calc = function(
    onUpdate = () => {}, 
    getConfig = () => ({})
) {
    const calculator = this;
    const $element = $(calculator);
    
    // ----------------------
    // بخش ۱: مدیریت سبد محاسبات
    // ----------------------
    calculator.isEmptyCart = () => $element.find(".cart-row").length === 0;
    
    calculator.getCartAdded = () => $element.find(".cart-row");
    
    calculator.getCartAddedObj = () => {
        return calculator.getCartAdded().map((_, row) => {
            const data = $(row).data();
            return Object.keys(data).reduce((obj, key) => {
                obj[key.replace("row_", "")] = data[key];
                return obj;
            }, {});
        }).get();
    };
    
    calculator.addToCart = (item) => {
        const cartConfig = env.calc.input.find(i => i.cart)?.cart || [];
        const row = $('<div class="col-12 cart-row mb-1"></div>');
        
        // ایجاد محتوای سبد
        let content = "";
        Object.entries(item).forEach(([key, value]) => {
            const config = cartConfig.find(c => c.key === key);
            if (config) content += `${config.label} - <b>${value}</b> ${config.unit} | `;
        });
        content = content.replace(/ \| $/, "");
        
        // ساخت ساختار سبد
        const rowContent = $(`
            <div class="row">
                <div class="col cart-row-delete-cont">
                    <button class="cart-row-delete btn btn-sm btn-outline-danger">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
                <div class="col">${content}</div>
            </div>
        `);
        
        // افزودن داده‌ها به سبد
        Object.entries(item).forEach(([key, value]) => {
            row.attr(`data-row_${key}`, value);
        });
        
        row.append(rowContent);
        $element.find(".cart").append(row);
        onUpdate();
    };

    // ----------------------
    // بخش ۲: مدیریت UI و ورودی‌ها
    // ----------------------
    calculator.toggleInputElement = (id, show) => {
        const action = show ? "show" : "hide";
        const $el = $(`#${id}`);
        
        if (id.startsWith("div_")) {
            $el[action]();
        } else {
            $(`[data-p="${id}"]`)[action]();
            $(`label[for="${id}"]`)[action]();
            $el.parents(".input-control")[action]();
        }
    };
    
    calculator.showInputElement = (id) => calculator.toggleInputElement(id, true);
    calculator.hideInputElement = (id) => calculator.toggleInputElement(id, false);

    // ----------------------
    // بخش ۳: ذخیره‌سازی و بازیابی داده‌ها
    // ----------------------
    const storage = {
        useLocalStorage: () => env.calc.ls,
        
        get: () => {
            const data = storage.useLocalStorage() 
                ? localStorage.getItem(env.calc.id)
                : $element.find(".calc-ls").text();
            return data ? JSON.parse(data) : null;
        },
        
        save: () => {
            if (storage.useLocalStorage()) {
                localStorage.setItem(env.calc.id, JSON.stringify({
                    input: $element.dataValues("data-p", false, ".calc-allow-ls"),
                    cart: calculator.getCartAddedObj()
                }));
            }
        },
        
        load: () => {
            const savedData = storage.get();
            if (!savedData) return;
            
            // بازیابی ورودی‌ها
            Object.entries(savedData.input).forEach(([key, value]) => {
                const $input = $(`[data-p="${key}"]`);
                if (!$input.length) return;
                
                if ($input.is("input[type='checkbox']")) {
                    $input.prop("checked", value);
                    const $target = $element.find(`[data-p="${$input.attr("data-trigger")}"]`);
                    calculator.triggerCheck($input, $target);
                } else {
                    $input.val(value || 0);
                }
            });
            
            // بازیابی سبد
            savedData.cart.forEach(item => calculator.addToCart(item));
        }
    };

    // ----------------------
    // بخش ۴: توابع محاسباتی پیشرفته
    // ----------------------
    calculator.linearInterpolation = (x0, x, x1, y0, y1) => {
        return y0 + ((y1 - y0) / (x1 - x0)) * (x - x0);
    };
    
    calculator.waterDilution = (initialConc, volume, targetConc) => {
        // محاسبات رقیق‌سازی با آب
        const initialMass = volume * calculator.getDensity(initialConc);
        const waterVolume = initialMass * (initialConc - targetConc) / targetConc;
        return {
            waterVolume,
            finalVolume: volume + waterVolume,
            concentrationChange: Math.abs(initialConc - targetConc)
        };
    };
    
    calculator.getDensity = (concentration) => {
        // محاسبه چگالی بر اساس غلظت
        const tableData = tables.tpm20;
        const concentrations = tableData.map(d => d.m);
        
        if (concentrations.includes(concentration)) {
            return parseFloat(tableData.find(d => d.m === concentration).p);
        }
        
        // درون‌یابی خطی
        const lower = Math.max(...concentrations.filter(c => c < concentration));
        const upper = Math.min(...concentrations.filter(c => c > concentration));
        const lowerDensity = parseFloat(tableData.find(d => d.m === lower).p);
        const upperDensity = parseFloat(tableData.find(d => d.m === upper).p);
        
        return calculator.linearInterpolation(
            lower, concentration, upper, 
            lowerDensity, upperDensity
        );
    };

    // ----------------------
    // بخش ۵: مدیریت رویدادها و راه‌اندازی
    // ----------------------
    const setupEvents = () => {
        $element
            .on("input", "input", handleInputChange)
            .on("change", "select", handleInputChange)
            .on("click", ".input-plus, .input-minus", handleCounterClick)
            .on("click", ".cart-row-delete", deleteCartItem)
            .on("click", ".cart-add", addToCart);
        
        // سایر رویدادها...
    };
    
    const handleInputChange = () => {
        onUpdate();
        storage.save();
    };
    
    const handleCounterClick = function() {
        const $btn = $(this);
        const $input = $btn.parent().find("input");
        const step = parseFloat($btn.parent().attr("data-input-control-step") || 1;
        const precision = parseInt($btn.parent().attr("data-input-control-round") || 0;
        let value = parseFloat($input.val()) || 0;
        
        value = $btn.hasClass("input-plus") 
            ? value + step 
            : value - step;
        
        $input.val(value.toFixed(precision));
        onUpdate();
        storage.save();
    };
    
    const deleteCartItem = function() {
        $(this).closest(".cart-row").remove();
        onUpdate();
        storage.save();
    };
    
    const addToCart = () => {
        // منطق جمع‌آوری داده‌ها از فرم
        const formData = {};
        calculator.addToCart(formData);
        storage.save();
    };

    // ----------------------
    // راه‌اندازی اولیه
    // ----------------------
    const initialize = () => {
        // ساخت UI
        createInputElements();
        createSharedElements();
        createSavedElements();
        
        // بارگذاری داده‌ها
        storage.load();
        
        // فعال‌سازی رویدادها
        setupEvents();
        
        // اولین محاسبه
        onUpdate();
    };

    // انتظار برای بارگذاری منابع
    waitForResources().then(initialize);
    
    return calculator;
};