<script>
    // 定义表单数据
    import { createEventDispatcher } from 'svelte';

    let problemDescription = "";
    let timeFrame = "";
    let contextualInformation = "";
    let stakeholderFeedback = "";
    let specificMetrics = "";
    const dispatch = createEventDispatcher();

    // 预填充表单内容的函数
    function fillForm(caseNumber) {
      switch (caseNumber) {
        case 1:
          problemDescription = "The XYZ mixer failed during operation, causing a halt in production.";
          timeFrame = "Over the past two weeks";
          contextualInformation = "No recent changes in the mixer's maintenance schedule.";
          stakeholderFeedback = "Operators reported unusual noises before the failure.";
          specificMetrics = "3 out of 5 batches were affected.";
          break;
        case 2:
          problemDescription = "Product B failed potency tests in the last quality control check.";
          timeFrame = "Over the past month";
          contextualInformation = "A new raw material supplier was introduced last month.";
          stakeholderFeedback = "Quality control team noted inconsistencies in raw material quality.";
          specificMetrics = "10% of batches failed potency tests.";
          break;
        case 3:
          problemDescription = "Packaging defects were observed in Product C, leading to customer complaints.";
          timeFrame = "Over the past three months";
          contextualInformation = "A new packaging machine was installed three months ago.";
          stakeholderFeedback = "Production team reported frequent jams in the new machine.";
          specificMetrics = "15% of units had packaging defects.";
          break;
        default:
          // 清空表单
          problemDescription = "";
          timeFrame = "";
          contextualInformation = "";
          stakeholderFeedback = "";
          specificMetrics = "";
      }
    }
  
    // 提交表单的函数
    const submitForm=async() =>{
      const formData = {
        problemDescription,
        timeFrame,
        contextualInformation,
        stakeholderFeedback,
        specificMetrics,
      };
      console.log("Form Data Submitted:", formData);
      dispatch("submit",formData);
      alert("Root Cause Analysis Submitted!");
    }
  </script>
  
  <style>
    .form-container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: #f9f9f9;
    }
    .form-header {
      font-size: 1.2em;
      margin-bottom: 20px;
    }
    .form-section {
      margin-bottom: 15px;
    }
    .form-section label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .form-section textarea {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      resize: vertical;
    }
    .button-group {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
    }
    .button-group button {
      padding: 10px 15px;
      border: none;
      border-radius: 4px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }
    .button-group button:hover {
      background-color: #0056b3;
    }
    .submit-button {
      width: 100%;
      padding: 10px;
      background-color: #28a745;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .submit-button:hover {
      background-color: #218838;
    }
  </style>
  
  <div class="form-container">
    <!-- 表头说明 -->
    <div class="form-header">
      <h2>Root Cause Assistant</h2>
      <p>
        Use this tool to perform a root cause analysis of quality issues, leading to improved compliance, cost savings, and proactive management of quality issues.
      </p>
      <h3>Root Cause Analysis Form</h3>
      <p>
        Instructions: Select a Use Case to prefill the form, then click 'Perform Root Cause Analysis'.
      </p>
    </div>
  
    <!-- 预填充按钮 -->
    <div class="button-group">
      <button on:click={() => fillForm(1)}>Case 1: The XYZ mixer failed</button>
      <button on:click={() => fillForm(2)}>Case 2: Product B Potency Failure</button>
      <button on:click={() => fillForm(3)}>Case 3: Packaging Defects in Product C</button>
    </div>
  
    <!-- 表单内容 -->
    <div class="form-section">
      <label for="problemDescription">Problem Description:</label>
      <textarea
        id="problemDescription"
        bind:value={problemDescription}
        rows="4"
        placeholder="Describe the issue in detail. What is happening? How often? What are the immediate impacts?"
      ></textarea>
    </div>
  
    <div class="form-section">
      <label for="timeFrame">Time Frame:</label>
      <textarea
        id="timeFrame"
        bind:value={timeFrame}
        rows="2"
        placeholder="Specify the period over which the problem has been observed (e.g., 'Over the past three months')."
      ></textarea>
    </div>
  
    <div class="form-section">
      <label for="contextualInformation">Contextual Information:</label>
      <textarea
        id="contextualInformation"
        bind:value={contextualInformation}
        rows="4"
        placeholder="Include any relevant background information, such as recent changes in processes, materials, or suppliers."
      ></textarea>
    </div>
  
    <div class="form-section">
      <label for="stakeholderFeedback">Stakeholder Feedback:</label>
      <textarea
        id="stakeholderFeedback"
        bind:value={stakeholderFeedback}
        rows="4"
        placeholder="Provide feedback or observations from relevant stakeholders involved in the process."
      ></textarea>
    </div>
  
    <div class="form-section">
      <label for="specificMetrics">Specific Metrics:</label>
      <textarea
        id="specificMetrics"
        bind:value={specificMetrics}
        rows="2"
        placeholder="Enter quantitative data related to the problem (e.g., '15% of batches have failed quality control checks due to contamination')."
      ></textarea>
    </div>
  
    <!-- 提交按钮 -->
    <button class="submit-button" type="submit"  on:click={submitForm}>Perform Root Cause Analysis</button>
  </div>