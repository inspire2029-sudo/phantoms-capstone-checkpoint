-- W2D5 SQL Debugging Solution

-- المشكلة الأولى
-- الشرط على order_status موجود في WHERE
-- ده بيشيل الصفوف اللي ملهاش order مطابق
-- وبالتالي ال LEFT JOIN هنا بيتصرف عمليا زي INNER JOIN بالنسبة للشرط ده

-- الحل
-- ننقل الشرط بتاع order_status من WHERE لل ON
-- كده كل العملاء يفضلوا موجودين حتى لو معندهمش طلبات COMPLETED

-- المشكلة الثانية
-- customer_name موجود في SELECT لكنه مش موجود في GROUP BY
-- في قواعد بيانات أو أوضاع SQL صارمة ده ممكن يسبب خطأ
-- والحل إننا نضيف customer_name لل GROUP BY

-- COALESCE هنا بتخلي العميل اللي معندوش طلبات COMPLETED ياخد صفر بدل NULL

SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
   AND o.order_status = 'COMPLETED'
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    c.customer_id;
