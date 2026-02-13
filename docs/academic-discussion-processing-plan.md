# Academic Discussion 题目批量处理计划

**来源文件夹：** `/Users/tengda/Downloads/学术讨论写作/`  
**题目总数：** 88 个  
**目标：** 全部录入到 `docs/academic-discussion-question-bank.md`，然后转换为 JSON

---

## 题目列表（88个）

### 第1批：前10题（测试流程）

1. Automation
2. Being An Early Adopter
3. Benefits of Switching Jobs Often
4. Businesspeople Should Learn Sales Techniques Or Management Skills？
5. Buy Goods Made in Their Own Country
6. Buying Used Or Recycled Products
7. Car-free Central Zones
8. Career or Relationships Imapcting Happiness
9. Celebrities or Ordinary People Taking about Products as Advertising Strategies
10. Children's Caring for Pets

### 第2批：11-20题

11. Cities Try to Save Historic Buildings
12. Continual Risks as Business Strategy
13. Customer Reviews for Deciding Buying Products
14. Developing Soft Skills - Nonacademic Skills
15. Difference between People from Different Countries Increasing Or Diminishing？
16. Do many possissions actually drecrease quality of life
17. Effects of Society Progress Happening Too Quickly
18. Environmental Tax on Air Travel
19. Excessive Consumption
20. Factories Or Individuals to Make Efforts for Environmental Protection

### 第3批：21-30题

21. Financial Support to Artists
22. Flexible Work Schedules
23. Four-day Workweek
24. Government Should Charge Drivers Fees for Driving during Rush Hour？
25. Government Should Keep Fuel Prices Low
26. Governments Encourage More Use of Electric Vehicles
27. Governments Or Companies Regulate Social Media Platform
28. Governments Should Not Keep Scientific Discoveries Secret
29. Hire Experienced Veterans Or Younger Employees
30. How Much Can Individuals Solve Water Pollution V.S. Large Institution

### 第4批：31-40题

31. Human Teachers Will Be Replaced？
32. Imposing Taxes and Fines to Stop Companies from Harming the Environment
33. Improve Schoolteachers' Salaries or Additional Resources
34. Job-Sharing Arrangement
35. Journalism Being Negatively Affected？
36. Lecturing Is An Effective Teaching Method？
37. Lecturing or Project-based Learning
38. Limiting Teaching of Fictional Texts
39. Living in One Town or City All Your Life
40. Local or Regional Government Reducing Spending

### 第5批：41-50题

41. Make Plans to Spend Time off from Work or School
42. Making Purchasing Decisions
43. Motivating Young Students：Activities, Or Playtime
44. New, Innovative Subjects Should Be Taught in Public Schools
45. Online Classes, Or Traditional In-person Classes？
46. Online Shopping Is Affecting Society？
47. Participation in Team Sports Important for A Child's Development？
48. Poor Eating Habit to Change
49. Pursue An Advanced Degree While Working Full-time？
50. Pursuing Degree Full-time Or Continuing Work and Studying Part-time

### 第6批：51-60题

51. Raising the cost of Fuel for Cars
52. Requiring First-year Students to Take A Course on Good Study Habits
53. Requiring Volunteer Work for Graduation
54. School Curriculum Must Include Classes in Art and Music
55. Setting A Minimum age for Children to Have Mobile Phones
56. Several Shorter Certification Or A University Degree？
57. Shop at Small Local Stores Or Superstores
58. Social Media Influencers
59. Space Exploration
60. Spend More Money on Art+Music Museums, Or Playgrounds and Public Swimming Pools

### 第7批：61-70题

61. Spending Time with A Close-knit Few Or A Larger Group of Friends
62. Students Exploring Nature and Learning about Environment
63. Students Should Be Allowed to Choose Their Own Field of Study
64. TV or books
65. Take Breaks from Reading Or Watching News
66. The Best Way to Determine Whether the Information Is Accurate
67. The Best Way to Make New Friends
68. The Biggest Disadvantage of Starting One's Own Business
69. The Greatest Impact on Protecting Environment for One Person
70. The Most Important Action for Leaders to Improve Country's Prosperity

### 第8批：71-80题

71. The Most Important Criteria for Promotion
72. The Most Important Factor for Employer to Consider When Deciding where Employees Should Work
73. The Most Important Subject
74. The Most Important Thing University Should Consider When Making Spending
75. The Most Important Thing to Maintain Good Health
76. To-do Lists Are Beneficial Tools for Learning and Working？
77. Using A Mobile App to Learn A Foreign Language
78. Using Cash to Make Purchase
79. Watching Online Videos Is Harmful to Children？
80. Watching Sports Or Following Their Favorite Team

### 第9批：81-88题（最后一批）

81. What Approach That Governments Can Use to Attract More People to Live in Rural Areas
82. What Companies Can Do To Be Attractive to Potential Employees
83. What Factors Should Be Taken into Account When Choosing Local Or International Charity Organizations
84. What Schools Can Do to Make Transition to A New School Easier
85. What Strategy Should Teachers Use to Increase High School Students' Interest in Learning
86. Why People Choose Not To Help Others - Inaction
87. Why People Choose to Live in Rural Areas
88. [待确认]

---

## 处理流程

### 每批处理步骤：

1. **查看截图**
   - 打开题目文件夹
   - 找到最清晰的截图（通常是题目名称命名的.png文件）
   - 确认包含：Professor Question + 2个Student Posts

2. **提取文字**
   - 从截图中提取Professor Question
   - 提取2个Student Posts（Author + Text）
   - 确认完整性

3. **录入题库**
   - 在 `docs/academic-discussion-question-bank.md` 中添加题目
   - 使用模板格式
   - 标记状态为 ⏳

4. **复制截图**
   - 将截图复制到 `docs/academic-discussion/images/`
   - 命名格式：`d{编号}-{简短名称}.png`（如：`d07-automation.png`）

5. **验证**
   - 检查格式是否正确
   - 确认所有字段完整
   - 标记状态为 ✅

### 批量转换

每完成一批（10题），运行：
```bash
python3 scripts/convert-question-bank-to-json.py
```

---

## 分类建议

根据题目主题，建议分类：

- **Education** (教育类)
  - Limiting Teaching of Fictional Texts
  - Requiring First-year Students to Take A Course on Good Study Habits
  - Requiring Volunteer Work for Graduation
  - School Curriculum Must Include Classes in Art and Music
  - The Most Important Subject
  - Human Teachers Will Be Replaced？
  - Lecturing or Project-based Learning
  - Online Classes, Or Traditional In-person Classes？
  - New, Innovative Subjects Should Be Taught in Public Schools
  - Students Should Be Allowed to Choose Their Own Field of Study
  - 等等...

- **Society** (社会类)
  - The Best Way to Make New Friends
  - Spending Time with A Close-knit Few Or A Larger Group of Friends
  - Living in One Town or City All Your Life
  - Why People Choose Not To Help Others - Inaction
  - 等等...

- **Environment** (环境类)
  - Environmental Tax on Air Travel
  - Factories Or Individuals to Make Efforts for Environmental Protection
  - The Greatest Impact on Protecting Environment for One Person
  - Imposing Taxes and Fines to Stop Companies from Harming the Environment
  - Car-free Central Zones
  - 等等...

- **Economy** (经济类)
  - Benefits of Switching Jobs Often
  - Businesspeople Should Learn Sales Techniques Or Management Skills？
  - Buy Goods Made in Their Own Country
  - Making Purchasing Decisions
  - 等等...

- **Technology** (科技类)
  - Automation
  - Being An Early Adopter
  - Human Teachers Will Be Replaced？
  - Using A Mobile App to Learn A Foreign Language
  - 等等...

---

## 进度跟踪

- [ ] 第1批（1-10）：⏳ 待处理
- [ ] 第2批（11-20）：⏳ 待处理
- [ ] 第3批（21-30）：⏳ 待处理
- [ ] 第4批（31-40）：⏳ 待处理
- [ ] 第5批（41-50）：⏳ 待处理
- [ ] 第6批（51-60）：⏳ 待处理
- [ ] 第7批（61-70）：⏳ 待处理
- [ ] 第8批（71-80）：⏳ 待处理
- [ ] 第9批（81-88）：⏳ 待处理

**总计：** 0/88 已完成

---

*创建时间：2026-02-13*
