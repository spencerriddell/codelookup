import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class SASCodeGenerator extends JFrame {

    private static final String SAS_TEMPLATE = """
            /* {var_value} */
            data new_varxx;
            YearNum = 2023;
            VarValID = {varvalid};
            Topic_ID = {topic_id};
            SubTopic_ID = {subtopic_id};
            ExcludeInclude = 1;
            SortOrder = 1;
            Topic_SortOrder = 1;
            SubTopic_SortOrder = 1;
            Topic_DefaultID = 1;
            DefaultID = 1;
            Indicator_SortOrder = ;
            YearDate = "2023-01-01";
            Dataset = "{dataset}";
            Dataset_Name = "{dataset_name}";
            Dataset_Type = "Health Surveys";
            VarCode = "{var_code}";
            VarValue = "{var_value}";
            VarType = "{var_type}";
            VarName = "{var_name}";
            Description = "{description}";
            Topic = "{topic}";
            Sub_Topic = "{sub_topic}";
            PopulationDatasource = "{population}";
            Note1 = "";
            Note2 = "";
            Note3 = "";
            CrossNotes = "";
            MapTitlePrefix = "";
            MapTitleSuffix = "";
            MapInsert = "";
            VarComments = "";
            Tag = "{var_name}_{tag_suffix}";
            DefaultPopulationSource = "{population}";
            output;
            run;
            """;

    // Data models
    static class Survey {
        String fullName;
        String population;
        String tagSuffix;
        Survey(String fullName, String population, String tagSuffix) {
            this.fullName = fullName;
            this.population = population;
            this.tagSuffix = tagSuffix;
        }
    }

    static class Topic {
        int id;
        Map<String, Integer> subtopics = new LinkedHashMap<>();
        Topic(int id) { this.id = id; }
    }

    static class VariableData {
        String dataset;       // short code, e.g., YRBS
        String datasetName;   // full name
        String population;
        String tagSuffix;

        String varCode;
        String varName;
        String description;
        String varType;       // Indicator | Demographic

        String topic;
        String subTopic;
        int topicId;
        int subtopicId;

        List<String> levels = new ArrayList<>();
    }

    private static final Map<String, Survey> SURVEYS = new LinkedHashMap<>();
    private static final Map<String, Topic> TOPICS = new LinkedHashMap<>();

    static {
        // Surveys
        SURVEYS.put("YRBS", new Survey("NYC Youth Risk Behavior Survey", "Youth", "YRBS"));
        SURVEYS.put("CHS", new Survey("Community Health Survey", "Adult", "CHS"));
        SURVEYS.put("HANES", new Survey("NYC Health and Nutrition Examination Survey", "Adult", "HANES"));
        SURVEYS.put("CCHS", new Survey("NYC Child Health Data", "Youth", "CCHS"));

        // Topics (mirrors the Python dict)
        Topic tChildren = new Topic(5);
        tChildren.subtopics.put("Child Development and Disabilities", 26);
        tChildren.subtopics.put("Day Care and School", 34);
        tChildren.subtopics.put("Drug and Alcohol Use", 10);
        tChildren.subtopics.put("Health Care Use", 17);
        tChildren.subtopics.put("Health Insurance", 15);
        tChildren.subtopics.put("Household and Neighborhood", 16);
        tChildren.subtopics.put("Health Status", 18);
        tChildren.subtopics.put("Mental Health", 3);
        tChildren.subtopics.put("Nutrition", 23);
        tChildren.subtopics.put("Physical Activity", 35);
        tChildren.subtopics.put("Physical Health Conditions", 12);
        tChildren.subtopics.put("Population Characteristics", 11);
        tChildren.subtopics.put("Safety", 4);
        tChildren.subtopics.put("Sleep", 33);
        tChildren.subtopics.put("Sexual Behavior", 30);
        tChildren.subtopics.put("Smoking", 7);
        tChildren.subtopics.put("Violence", 1);
        TOPICS.put("Children and Youth", tChildren);

        Topic tHealthy = new Topic(4);
        tHealthy.subtopics.put("Vaccinations", 29);
        tHealthy.subtopics.put("Drug and Alcohol Use", 10);
        tHealthy.subtopics.put("Health Status", 18);
        tHealthy.subtopics.put("Nutrition", 23);
        tHealthy.subtopics.put("Physical Activity", 35);
        tHealthy.subtopics.put("Safety", 4);
        tHealthy.subtopics.put("Screening", 19);
        tHealthy.subtopics.put("Sexual Behavior", 30);
        TOPICS.put("Healthy Living", tHealthy);

        TOPICS.put("Sleep", new Topic(33));
        TOPICS.put("Smoking", new Topic(7));
        TOPICS.put("Vaccinations", new Topic(29));
        TOPICS.put("Violence", new Topic(1));

        Topic tCommunity = new Topic(6);
        tCommunity.subtopics.put("Day Care and School", 34);
        tCommunity.subtopics.put("Economic Factors", 31);
        tCommunity.subtopics.put("Population Characteristics", 11);
        tCommunity.subtopics.put("Social Factors", 13);
        TOPICS.put("Community Characteristics", tCommunity);

        Topic tLiving = new Topic(7);
        tLiving.subtopics.put("Built Environment", 28);
        tLiving.subtopics.put("Housing", 14);
        TOPICS.put("Living and Environmental Conditions", tLiving);

        TOPICS.put("Safety", new Topic(4));
        TOPICS.put("Social Factors", new Topic(13));

        Topic tMental = new Topic(3);
        tMental.subtopics.put("Drug and Alcohol Use", 10);
        tMental.subtopics.put("Mental Health Conditions", 20);
        tMental.subtopics.put("Mental Health Counseling and Treatment", 27);
        TOPICS.put("Mental Health", tMental);

        Topic tDisease = new Topic(1);
        tDisease.subtopics.put("Child Development and Disabilities", 26);
        tDisease.subtopics.put("Chronic Diseases", 24);
        tDisease.subtopics.put("Dental Health", 21);
        tDisease.subtopics.put("Foodborne or Waterborne Infections", 43);
        tDisease.subtopics.put("HIV-AIDS", 8);
        tDisease.subtopics.put("Hearing and Vision Health", 36);
        tDisease.subtopics.put("Hepatitis Infections", 48);
        tDisease.subtopics.put("Invasive Bacterial Infections", 45);
        tDisease.subtopics.put("Mosquitoborne Infections", 37);
        tDisease.subtopics.put("Other and Rare Diseases", 46);
        tDisease.subtopics.put("Person-to-Person Infections", 44);
        tDisease.subtopics.put("Respiratory Infections", 41);
        tDisease.subtopics.put("Sexually Transmitted Infections", 5);
        tDisease.subtopics.put("Syndromic Surveillance", 39);
        tDisease.subtopics.put("Tickborne Infections", 42);
        tDisease.subtopics.put("Tuberculosis", 53);
        tDisease.subtopics.put("Vaccine-Preventable Diseases", 47);
        tDisease.subtopics.put("Zoonotic Infections", 40);
        TOPICS.put("Diseases and Conditions", tDisease);

        Topic tAccess = new Topic(2);
        tAccess.subtopics.put("Health Care Use", 17);
        tAccess.subtopics.put("Health Insurance", 15);
        tAccess.subtopics.put("Mental Health Counseling and Treatment", 27);
        tAccess.subtopics.put("Screening", 19);
        tAccess.subtopics.put("Vaccinations", 29);
        TOPICS.put("Health Care Access and Use", tAccess);

        Topic tBirth = new Topic(8);
        tBirth.subtopics.put("Birth", 38);
        tBirth.subtopics.put("Infant Mortality", 51);
        tBirth.subtopics.put("Leading Cause of Death", 52);
        tBirth.subtopics.put("Mortality and Premature Mortality", 49);
        TOPICS.put("Birth and Death", tBirth);
    }

    // UI components
    private JComboBox<String> datasetCombo;
    private JTextField varCodeField;
    private JTextField varNameField;
    private JTextField descriptionField;

    private JComboBox<String> varTypeCombo;
    private JComboBox<String> topicCombo;
    private JComboBox<String> subtopicCombo;

    private JComboBox<String> levelsCombo;
    private JPanel levelNamesPanel;
    private final List<JTextField> levelFields = new ArrayList<>();

    private JButton prevBtn;
    private JButton nextBtn;
    private JButton addVarBtn;
    private JButton deleteVarBtn;
    private JButton generateBtn;

    // State
    private final List<VariableData> variables = new ArrayList<>();
    private int currentVarIndex = -1;

    public SASCodeGenerator() {
        super("SAS Code Generator");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(900, 750);
        setLocationRelativeTo(null);
        buildUI();
        initializeDefaults();
    }

    private void buildUI() {
        JPanel root = new JPanel();
        root.setLayout(new BorderLayout());

        JPanel content = new JPanel();
        content.setLayout(new BoxLayout(content, BoxLayout.Y_AXIS));
        content.setBorder(new EmptyBorder(15, 15, 15, 15));

        // Dataset selection
        content.add(label("Select Survey Dataset:"));
        datasetCombo = new JComboBox<>(SURVEYS.keySet().toArray(new String[0]));
        content.add(fillX(datasetCombo));
        datasetCombo.addActionListener(e -> onSurveyChange());

        // Variable Code
        content.add(space(10));
        content.add(label("Variable Code:"));
        varCodeField = new JTextField();
        content.add(fillX(varCodeField));

        // Variable Name
        content.add(space(10));
        content.add(label("Variable Name:"));
        varNameField = new JTextField();
        content.add(fillX(varNameField));

        // Description
        content.add(space(10));
        content.add(label("Description:"));
        descriptionField = new JTextField();
        content.add(fillX(descriptionField));

        // Variable Type
        content.add(space(10));
        content.add(label("Variable Type:"));
        varTypeCombo = new JComboBox<>(new String[] {"Indicator", "Demographic"});
        content.add(fillX(varTypeCombo));
        varTypeCombo.addActionListener(e -> onVarTypeChange());

        // Topic
        content.add(space(10));
        content.add(label("Topic:"));
        topicCombo = new JComboBox<>(TOPICS.keySet().toArray(new String[0]));
        topicCombo.setSelectedItem(null);
        content.add(fillX(topicCombo));
        topicCombo.addActionListener(e -> onTopicChange());

        // Subtopic
        content.add(space(10));
        content.add(label("Sub-Topic:"));
        subtopicCombo = new JComboBox<>();
        content.add(fillX(subtopicCombo));

        // Number of levels
        content.add(space(10));
        content.add(label("Number of Levels:"));
        levelsCombo = new JComboBox<>(new String[]{"2", "3", "4", "5", "6"});
        content.add(fillX(levelsCombo));
        levelsCombo.addActionListener(e -> onLevelsChange());

        // Level names panel
        levelNamesPanel = new JPanel(new GridBagLayout());
        content.add(space(5));
        content.add(fillX(levelNamesPanel));

        // Navigation
        JPanel nav = new JPanel(new FlowLayout(FlowLayout.LEFT));
        prevBtn = new JButton("← Previous Variable");
        nextBtn = new JButton("Next Variable →");
        addVarBtn = new JButton("Add Another Variable");
        deleteVarBtn = new JButton("Delete Current Variable");

        nav.add(prevBtn);
        nav.add(nextBtn);
        nav.add(Box.createHorizontalStrut(10));
        nav.add(addVarBtn);
        nav.add(Box.createHorizontalStrut(10));
        nav.add(deleteVarBtn);

        prevBtn.addActionListener(e -> prevVariable());
        nextBtn.addActionListener(e -> nextVariable());
        addVarBtn.addActionListener(e -> addVariable());
        deleteVarBtn.addActionListener(e -> deleteVariable());

        content.add(space(5));
        content.add(fillX(nav));

        // Generate button
        generateBtn = new JButton("Generate SAS Code");
        JPanel genWrap = new JPanel(new FlowLayout(FlowLayout.LEFT));
        genWrap.add(generateBtn);
        content.add(space(10));
        content.add(fillX(genWrap));
        generateBtn.addActionListener(e -> generateSasCode());

        // Footer
        JLabel footer = new JLabel("Made by Spencer Riddell, August 2025");
        footer.setForeground(new Color(0x66, 0x66, 0x66));
        footer.setFont(footer.getFont().deriveFont(footer.getFont().getSize2D() - 2));

        root.add(new JScrollPane(content), BorderLayout.CENTER);
        JPanel south = new JPanel(new FlowLayout(FlowLayout.CENTER));
        south.add(footer);
        root.add(south, BorderLayout.SOUTH);

        setContentPane(root);
    }

    private void initializeDefaults() {
        if (datasetCombo.getItemCount() > 0) datasetCombo.setSelectedIndex(0);
        varTypeCombo.setSelectedItem("Indicator");
        onSurveyChange();
        onVarTypeChange();
        loadVariable(0);
        updateNavButtons();
    }

    // Handlers

    private void onSurveyChange() {
        topicCombo.setSelectedItem(null);
        subtopicCombo.removeAllItems();
    }

    private void onVarTypeChange() {
        String vt = (String) varTypeCombo.getSelectedItem();
        boolean isDemo = "Demographic".equals(vt);
        topicCombo.setEnabled(!isDemo);
        subtopicCombo.setEnabled(!isDemo);
        if (isDemo) {
            topicCombo.setSelectedItem(null);
            subtopicCombo.removeAllItems();
        }
    }

    private void onTopicChange() {
        Object selected = topicCombo.getSelectedItem();
        subtopicCombo.removeAllItems();
        if (selected == null) return;
        Topic t = TOPICS.get((String) selected);
        if (t == null || t.subtopics.isEmpty()) return;
        for (String name : t.subtopics.keySet()) {
            subtopicCombo.addItem(name);
        }
        subtopicCombo.setSelectedItem(null);
    }

    private void onLevelsChange() {
        levelNamesPanel.removeAll();
        levelFields.clear();

        int n;
        try {
            n = Integer.parseInt((String) levelsCombo.getSelectedItem());
        } catch (Exception e) {
            levelNamesPanel.revalidate();
            levelNamesPanel.repaint();
            return;
        }

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(2,5,2,5);
        gbc.gridy = 0;
        for (int i = 0; i < n; i++) {
            gbc.gridx = 0;
            gbc.anchor = GridBagConstraints.WEST;
            levelNamesPanel.add(new JLabel("Level " + (i + 1) + " Name:"), gbc);

            gbc.gridx = 1;
            gbc.weightx = 1.0;
            gbc.fill = GridBagConstraints.HORIZONTAL;
            JTextField tf = new JTextField();
            levelNamesPanel.add(tf, gbc);
            levelFields.add(tf);

            gbc.gridy++;
            gbc.weightx = 0;
            gbc.fill = GridBagConstraints.NONE;
        }

        levelNamesPanel.revalidate();
        levelNamesPanel.repaint();
    }

    // Data management

    private boolean saveCurrentVariable() {
        String dataset = (String) datasetCombo.getSelectedItem();
        if (dataset == null || dataset.isBlank()) {
            error("Please select a Survey Dataset.");
            return false;
        }
        String varCode = varCodeField.getText().trim();
        if (varCode.isEmpty()) {
            error("Please enter Variable Code.");
            return false;
        }
        String varName = varNameField.getText().trim();
        if (varName.isEmpty()) {
            error("Please enter Variable Name.");
            return false;
        }
        String desc = descriptionField.getText().trim();
        if (desc.isEmpty()) {
            error("Please enter Description.");
            return false;
        }
        String varType = (String) varTypeCombo.getSelectedItem();
        if (varType == null || varType.isBlank()) {
            error("Please select Variable Type.");
            return false;
        }

        String topic = "";
        String subTopic = "";
        if ("Indicator".equals(varType)) {
            Object tSel = topicCombo.getSelectedItem();
            Object stSel = subtopicCombo.getSelectedItem();
            if (tSel == null || stSel == null) {
                error("Please select Topic and Sub-Topic for Indicators.");
                return false;
            }
            topic = (String) tSel;
            subTopic = (String) stSel;
        }

        int nLevels;
        try {
            nLevels = Integer.parseInt((String) levelsCombo.getSelectedItem());
        } catch (Exception e) {
            error("Please select Number of Levels.");
            return false;
        }
        List<String> levels = new ArrayList<>();
        for (int i = 0; i < nLevels; i++) {
            String v = (i < levelFields.size()) ? levelFields.get(i).getText().trim() : "";
            if (v.isEmpty()) {
                error("Please enter a name for Level " + (i + 1) + ".");
                return false;
            }
            levels.add(v);
        }

        Survey s = SURVEYS.get(dataset);
        VariableData data = new VariableData();
        data.dataset = dataset;
        data.datasetName = s.fullName;
        data.population = s.population;
        data.tagSuffix = s.tagSuffix;
        data.varCode = varCode;
        data.varName = varName;
        data.description = desc;
        data.varType = varType;
        data.topic = "Indicator".equals(varType) ? topic : "";
        data.subTopic = "Indicator".equals(varType) ? subTopic : "";

        if (data.topic != null && !data.topic.isBlank() && TOPICS.containsKey(data.topic)) {
            data.topicId = TOPICS.get(data.topic).id;
        } else {
            data.topicId = 0;
        }
        if ("Indicator".equals(varType)) {
            Topic tp = TOPICS.getOrDefault(topic, null);
            if (tp != null) {
                data.subtopicId = tp.subtopics.getOrDefault(subTopic, 0);
            } else {
                data.subtopicId = 0;
            }
        } else {
            data.subtopicId = 0;
        }

        data.levels = levels;

        if (0 <= currentVarIndex && currentVarIndex < variables.size()) {
            variables.set(currentVarIndex, data);
        } else {
            variables.add(data);
            currentVarIndex = variables.size() - 1;
        }

        return true;
    }

    private void loadVariable(int index) {
        if (variables.isEmpty() || index < 0 || index >= variables.size()) {
            clearForm();
            currentVarIndex = -1;
            updateNavButtons();
            return;
        }

        currentVarIndex = index;
        VariableData v = variables.get(index);

        datasetCombo.setSelectedItem(v.dataset);
        varCodeField.setText(v.varCode);
        varNameField.setText(v.varName);
        descriptionField.setText(v.description);

        varTypeCombo.setSelectedItem(v.varType);
        onVarTypeChange();

        topicCombo.setSelectedItem(v.topic.isBlank() ? null : v.topic);
        onTopicChange();
        if (!v.subTopic.isBlank()) {
            subtopicCombo.setSelectedItem(v.subTopic);
        } else {
            subtopicCombo.setSelectedItem(null);
        }

        levelsCombo.setSelectedItem(String.valueOf(v.levels.size()));
        onLevelsChange();
        for (int i = 0; i < Math.min(levelFields.size(), v.levels.size()); i++) {
            levelFields.get(i).setText(v.levels.get(i));
        }

        updateNavButtons();
    }

    private void clearForm() {
        if (datasetCombo.getItemCount() > 0) datasetCombo.setSelectedIndex(0);
        varCodeField.setText("");
        varNameField.setText("");
        descriptionField.setText("");
        varTypeCombo.setSelectedItem("");
        topicCombo.setSelectedItem(null);
        subtopicCombo.removeAllItems();
        levelsCombo.setSelectedItem(null);
        onLevelsChange();
        updateNavButtons();
    }

    // Navigation

    private void prevVariable() {
        if (currentVarIndex > 0) {
            if (!saveCurrentVariable()) return;
            loadVariable(currentVarIndex - 1);
        }
    }

    private void nextVariable() {
        if (currentVarIndex < variables.size() - 1) {
            if (!saveCurrentVariable()) return;
            loadVariable(currentVarIndex + 1);
        }
    }

    private void addVariable() {
        if (!saveCurrentVariable()) return;
        currentVarIndex = variables.size(); // new slot
        clearForm();
        if (!variables.isEmpty()) {
            deleteVarBtn.setEnabled(true);
        }
    }

    private void deleteVariable() {
        // No saved variables
        if (variables.isEmpty()) {
            if (!varCodeField.getText().isBlank() || !varNameField.getText().isBlank() || !descriptionField.getText().isBlank()) {
                int res = JOptionPane.showConfirmDialog(this,
                        "No variables saved yet.\nClear the current form?",
                        "Clear Form",
                        JOptionPane.YES_NO_OPTION);
                if (res != JOptionPane.YES_OPTION) return;
            }
            clearForm();
            currentVarIndex = -1;
            updateNavButtons();
            return;
        }

        // Index invalid
        if (currentVarIndex < 0 || currentVarIndex >= variables.size()) {
            JOptionPane.showMessageDialog(this, "No current variable selected to delete.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String name = variables.get(currentVarIndex).varName;
        int res = JOptionPane.showConfirmDialog(this,
                "Are you sure you want to delete variable '" + name + "'?\n\nThis action cannot be undone.",
                "Confirm Delete",
                JOptionPane.YES_NO_OPTION);
        if (res != JOptionPane.YES_OPTION) return;

        variables.remove(currentVarIndex);

        if (variables.isEmpty()) {
            currentVarIndex = -1;
            clearForm();
        } else if (currentVarIndex >= variables.size()) {
            currentVarIndex = variables.size() - 1;
            loadVariable(currentVarIndex);
        } else {
            loadVariable(currentVarIndex);
        }

        updateNavButtons();
        JOptionPane.showMessageDialog(this, "Variable '" + name + "' has been deleted.", "Success", JOptionPane.INFORMATION_MESSAGE);
    }

    private void updateNavButtons() {
        prevBtn.setEnabled(currentVarIndex > 0);
        nextBtn.setEnabled(currentVarIndex >= 0 && currentVarIndex < variables.size() - 1);
        deleteVarBtn.setEnabled(!variables.isEmpty() || currentVarIndex >= 0);
    }

    // Generate SAS

    private void generateSasCode() {
        if (!saveCurrentVariable()) return;
        if (variables.isEmpty()) {
            error("No variables to generate SAS code.");
            return;
        }

        StringBuilder sb = new StringBuilder();
        for (VariableData v : variables) {
            for (int i = 0; i < v.levels.size(); i++) {
                String lvl = v.levels.get(i);
                Map<String, String> m = new LinkedHashMap<>();
                m.put("varvalid", String.valueOf(i + 1));
                m.put("topic_id", String.valueOf(v.topicId));
                m.put("subtopic_id", String.valueOf(v.subtopicId));
                m.put("dataset", v.dataset);
                m.put("dataset_name", v.datasetName);
                m.put("var_code", v.varCode);
                m.put("var_value", escapeQuotes(lvl));
                m.put("var_type", v.varType);
                m.put("var_name", escapeQuotes(v.varName));
                m.put("description", escapeQuotes(v.description));
                m.put("topic", escapeQuotes(v.topic));
                m.put("sub_topic", escapeQuotes(v.subTopic));
                m.put("population", escapeQuotes(v.population));
                m.put("tag_suffix", escapeQuotes(v.tagSuffix));

                sb.append(renderTemplate(SAS_TEMPLATE, m)).append("\n");
            }
            sb.append("\n");
        }

        showOutputPopup(sb.toString().trim());
    }

    // Helpers

    private static String renderTemplate(String template, Map<String, String> values) {
        String out = template;
        for (Map.Entry<String, String> e : values.entrySet()) {
            out = out.replace("{" + e.getKey() + "}", e.getValue());
        }
        return out;
    }

    private static String escapeQuotes(String s) {
        if (s == null) return "";
        return s.replace("\"", "\"\"");
    }

    private void showOutputPopup(String text) {
        JDialog dlg = new JDialog(this, "Generated SAS Code", true);
        dlg.setSize(850, 650);
        dlg.setLocationRelativeTo(this);

        JTextArea area = new JTextArea(text);
        area.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        area.setWrapStyleWord(true);
        area.setLineWrap(true);
        area.setEditable(false);

        JScrollPane sp = new JScrollPane(area);
        dlg.setContentPane(sp);
        dlg.setVisible(true);
    }

    private static JLabel label(String text) {
        return new JLabel(text);
    }

    private static Component space(int h) {
        return Box.createVerticalStrut(h);
    }

    private static JComponent fillX(JComponent c) {
        c.setMaximumSize(new Dimension(Integer.MAX_VALUE, c.getPreferredSize().height));
        return c;
    }

    private static void error(String message) {
        JOptionPane.showMessageDialog(null, message, "Error", JOptionPane.ERROR_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new SASCodeGenerator().setVisible(true));
    }
}
