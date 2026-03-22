import { useState } from "react";
import { Input, Button, Card, Descriptions, Tag, message, Spin } from "antd";
import { ingestDialogue } from "../api/client";

const { TextArea } = Input;

export default function IngestPage() {
  const [dialogue, setDialogue] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!dialogue.trim()) {
      message.warning("Please paste a dialogue first");
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const res = await ingestDialogue(dialogue);
      setResult(res.data);
      message.success("Summary generated and saved successfully");
    } catch (err) {
      message.error(err.response?.data?.detail || "Failed to generate summary");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto" }}>
      <h2>Ingest Patient Dialogue</h2>

      <TextArea
        rows={10}
        placeholder="Paste patient-physician dialogue here..."
        value={dialogue}
        onChange={(e) => setDialogue(e.target.value)}
        disabled={loading}
      />

      <Button
        type="primary"
        onClick={handleSubmit}
        loading={loading}
        style={{ marginTop: 16 }}
      >
        {loading ? "Generating Summary..." : "Submit"}
      </Button>

      {loading && (
        <div style={{ textAlign: "center", marginTop: 24 }}>
          <Spin tip="LLM is processing the dialogue, this may take up to 1-2 minutes..." />
        </div>
      )}

      {result && (
        <Card title="Generated SOAP Summary" style={{ marginTop: 24 }}>
          <Descriptions column={1} bordered>
            <Descriptions.Item label="Patient Name">
              {result.summary.patient_name}
            </Descriptions.Item>
            <Descriptions.Item label="Age">
              {result.summary.age ?? "Unknown"}
            </Descriptions.Item>
            <Descriptions.Item label="Subjective">
              {result.summary.subjective}
            </Descriptions.Item>
            <Descriptions.Item label="Objective">
              {result.summary.objective}
            </Descriptions.Item>
            <Descriptions.Item label="Assessment">
              {result.summary.assessment}
            </Descriptions.Item>
            <Descriptions.Item label="Plan">
              {result.summary.plan}
            </Descriptions.Item>
            <Descriptions.Item label="Medications">
              {result.summary.medications.map((med) => (
                <Tag color="blue" key={med}>{med}</Tag>
              ))}
            </Descriptions.Item>
            <Descriptions.Item label="Diagnoses">
              {result.summary.diagnoses.map((d) => (
                <Tag color="red" key={d}>{d}</Tag>
              ))}
            </Descriptions.Item>
          </Descriptions>
          <p style={{ marginTop: 12, color: "#888" }}>
            Patient ID: {result.patient_id}
          </p>
        </Card>
      )}
    </div>
  );
}