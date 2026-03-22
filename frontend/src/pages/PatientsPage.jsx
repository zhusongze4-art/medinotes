import { useState, useEffect } from "react";
import { Input, Card, List, Modal, Descriptions, Tag, Empty, Spin } from "antd";
import { getPatients, getPatient, searchSimilar } from "../api/client";

const { Search } = Input;

export default function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [detail, setDetail] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [similar, setSimilar] = useState([]);

  const fetchPatients = async (query = "") => {
    setLoading(true);
    try {
      const res = await getPatients(query);
      setPatients(res.data);
    } catch {
      setPatients([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleCardClick = async (patientId) => {
    try {
      const res = await getPatient(patientId);
      setDetail(res.data);
      setModalOpen(true);

      const simRes = await searchSimilar(res.data.summary.assessment, 3);
      const filtered = simRes.data.results.filter(
        (r) => r.patient_id !== patientId
      );
      setSimilar(filtered);
    } catch {
      setDetail(null);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto" }}>
      <h2>Patient Database</h2>

      <Search
        placeholder="Search by patient name..."
        onSearch={fetchPatients}
        allowClear
        enterButton
        style={{ marginBottom: 24 }}
      />

      {loading ? (
        <Spin />
      ) : patients.length === 0 ? (
        <Empty description="No patients found" />
      ) : (
        <List
          grid={{ gutter: 16, column: 2 }}
          dataSource={patients}
          renderItem={(p) => (
            <List.Item>
              <Card
                hoverable
                title={`${p.patient_name} (${p.age ?? "N/A"})`}
                onClick={() => handleCardClick(p.patient_id)}
              >
                <p>{p.assessment}</p>
              </Card>
            </List.Item>
          )}
        />
      )}

      <Modal
        title={detail?.summary.patient_name}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        footer={null}
        width={700}
      >
        {detail && (
          <>
            <Descriptions column={1} bordered size="small">
              <Descriptions.Item label="Age">
                {detail.summary.age ?? "Unknown"}
              </Descriptions.Item>
              <Descriptions.Item label="Subjective">
                {detail.summary.subjective}
              </Descriptions.Item>
              <Descriptions.Item label="Objective">
                {detail.summary.objective}
              </Descriptions.Item>
              <Descriptions.Item label="Assessment">
                {detail.summary.assessment}
              </Descriptions.Item>
              <Descriptions.Item label="Plan">
                {detail.summary.plan}
              </Descriptions.Item>
              <Descriptions.Item label="Medications">
                {detail.summary.medications.map((m) => (
                  <Tag color="blue" key={m}>{m}</Tag>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="Diagnoses">
                {detail.summary.diagnoses.map((d) => (
                  <Tag color="red" key={d}>{d}</Tag>
                ))}
              </Descriptions.Item>
            </Descriptions>

            {similar.length > 0 && (
              <>
                <h4 style={{ marginTop: 20 }}>Similar Cases</h4>
                {similar.map((s) => (
                  <Card
                    key={s.patient_id}
                    size="small"
                    style={{ marginBottom: 8 }}
                    title={`Similarity: ${(s.similarity * 100).toFixed(1)}%`}
                  >
                    <p>{s.summary.substring(0, 200)}...</p>
                  </Card>
                ))}
              </>
            )}
          </>
        )}
      </Modal>
    </div>
  );
}