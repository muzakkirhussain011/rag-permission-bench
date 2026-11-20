# (g) The engine pre-filter and the store filter on the same pairs

Where A3 answered a subset of the pairs (shares 0.05, 0.2 and 0.5), A4 at the same setting on exactly the (job, user, question) pairs A3 answered, averaged per user and then over users.

| store | setting | layout | pairs | A3 recall | A4 recall, same pairs |
|---|---|---|---|---|---|
| pgvector | default | w3_s0p05_neg | 900 | 0.029 | 0.029 |
| pgvector | default | w3_s0p05_none | 900 | 0.271 | 0.271 |
| pgvector | default | w3_s0p05_pos | 900 | 0.457 | 0.457 |
| pgvector | default | w3_s0p2_neg | 300 | 0.236 | 0.236 |
| pgvector | default | w3_s0p2_none | 300 | 0.625 | 0.625 |
| pgvector | default | w3_s0p2_pos | 300 | 0.758 | 0.758 |
| pgvector | default | w3_s0p5_neg | 150 | 0.569 | 0.569 |
| pgvector | default | w3_s0p5_none | 150 | 0.902 | 0.902 |
| pgvector | default | w3_s0p5_pos | 150 | 0.898 | 0.898 |
| pgvector | iterative | w3_s0p05_neg | 900 | 0.608 | 0.608 |
| pgvector | iterative | w3_s0p05_none | 900 | 0.860 | 0.860 |
| pgvector | iterative | w3_s0p05_pos | 900 | 0.869 | 0.869 |
| pgvector | iterative | w3_s0p2_neg | 300 | 0.832 | 0.832 |
| pgvector | iterative | w3_s0p2_none | 300 | 0.873 | 0.873 |
| pgvector | iterative | w3_s0p2_pos | 300 | 0.920 | 0.920 |
| pgvector | iterative | w3_s0p5_neg | 150 | 0.852 | 0.852 |
| pgvector | iterative | w3_s0p5_none | 150 | 0.945 | 0.945 |
| pgvector | iterative | w3_s0p5_pos | 150 | 0.955 | 0.955 |
| qdrant | default | w3_s0p05_neg | 900 | 0.182 | 0.182 |
| qdrant | default | w3_s0p05_none | 900 | 0.562 | 0.562 |
| qdrant | default | w3_s0p05_pos | 900 | 0.770 | 0.770 |
| qdrant | default | w3_s0p2_neg | 300 | 0.485 | 0.485 |
| qdrant | default | w3_s0p2_none | 300 | 0.765 | 0.765 |
| qdrant | default | w3_s0p2_pos | 300 | 0.899 | 0.899 |
| qdrant | default | w3_s0p5_neg | 150 | 0.717 | 0.717 |
| qdrant | default | w3_s0p5_none | 150 | 0.915 | 0.915 |
| qdrant | default | w3_s0p5_pos | 150 | 0.936 | 0.936 |
| qdrant | acorn | w3_s0p05_neg | 900 | 0.660 | 0.660 |
| qdrant | acorn | w3_s0p05_none | 900 | 0.923 | 0.923 |
| qdrant | acorn | w3_s0p05_pos | 900 | 0.966 | 0.966 |
| qdrant | acorn | w3_s0p2_neg | 300 | 0.855 | 0.855 |
| qdrant | acorn | w3_s0p2_none | 300 | 0.965 | 0.965 |
| qdrant | acorn | w3_s0p2_pos | 300 | 0.973 | 0.973 |
| qdrant | acorn | w3_s0p5_neg | 150 | 0.717 | 0.932 |
| qdrant | acorn | w3_s0p5_none | 150 | 0.915 | 0.985 |
| qdrant | acorn | w3_s0p5_pos | 150 | 0.936 | 0.973 |
| milvus | default | w3_s0p05_neg | 900 | 1.000 | 1.000 |
| milvus | default | w3_s0p05_none | 900 | 1.000 | 1.000 |
| milvus | default | w3_s0p05_pos | 900 | 1.000 | 1.000 |
| milvus | default | w3_s0p2_neg | 300 | 0.955 | 0.955 |
| milvus | default | w3_s0p2_none | 300 | 0.966 | 0.966 |
| milvus | default | w3_s0p2_pos | 300 | 0.967 | 0.967 |
| milvus | default | w3_s0p5_neg | 150 | 0.917 | 0.917 |
| milvus | default | w3_s0p5_none | 150 | 0.963 | 0.963 |
| milvus | default | w3_s0p5_pos | 150 | 0.969 | 0.969 |
| milvus | iterative | w3_s0p05_neg | 900 | 0.929 | 0.929 |
| milvus | iterative | w3_s0p05_none | 900 | 0.944 | 0.944 |
| milvus | iterative | w3_s0p05_pos | 900 | 0.944 | 0.944 |
| milvus | iterative | w3_s0p2_neg | 300 | 0.910 | 0.910 |
| milvus | iterative | w3_s0p2_none | 300 | 0.944 | 0.944 |
| milvus | iterative | w3_s0p2_pos | 300 | 0.959 | 0.959 |
| milvus | iterative | w3_s0p5_neg | 150 | 0.935 | 0.935 |
| milvus | iterative | w3_s0p5_none | 150 | 0.973 | 0.973 |
| milvus | iterative | w3_s0p5_pos | 150 | 0.972 | 0.972 |
| weaviate | default | w3_s0p05_neg | 900 | 0.547 | 0.547 |
| weaviate | default | w3_s0p05_none | 900 | 0.823 | 0.823 |
| weaviate | default | w3_s0p05_pos | 900 | 0.888 | 0.888 |
| weaviate | default | w3_s0p2_neg | 300 | 0.738 | 0.738 |
| weaviate | default | w3_s0p2_none | 300 | 0.872 | 0.872 |
| weaviate | default | w3_s0p2_pos | 300 | 0.914 | 0.914 |
| weaviate | default | w3_s0p5_neg | 150 | 0.944 | 0.944 |
| weaviate | default | w3_s0p5_none | 150 | 0.960 | 0.960 |
| weaviate | default | w3_s0p5_pos | 150 | 0.961 | 0.961 |
| weaviate | pathseer | w3_s0p05_neg | 900 | 0.913 | 0.913 |
| weaviate | pathseer | w3_s0p05_none | 900 | 0.913 | 0.913 |
| weaviate | pathseer | w3_s0p05_pos | 900 | 0.927 | 0.927 |
| weaviate | pathseer | w3_s0p2_neg | 300 | 0.887 | 0.887 |
| weaviate | pathseer | w3_s0p2_none | 300 | 0.909 | 0.909 |
| weaviate | pathseer | w3_s0p2_pos | 300 | 0.944 | 0.944 |
| weaviate | pathseer | w3_s0p5_neg | 150 | 0.871 | 0.871 |
| weaviate | pathseer | w3_s0p5_none | 150 | 0.946 | 0.946 |
| weaviate | pathseer | w3_s0p5_pos | 150 | 0.960 | 0.960 |
| opensearch | default | w3_s0p05_neg | 900 | 1.000 | 1.000 |
| opensearch | default | w3_s0p05_none | 900 | 1.000 | 1.000 |
| opensearch | default | w3_s0p05_pos | 900 | 1.000 | 1.000 |
| opensearch | default | w3_s0p2_neg | 300 | 0.886 | 0.886 |
| opensearch | default | w3_s0p2_none | 300 | 0.970 | 0.970 |
| opensearch | default | w3_s0p2_pos | 300 | 0.978 | 0.978 |
| opensearch | default | w3_s0p5_neg | 150 | 0.958 | 0.958 |
| opensearch | default | w3_s0p5_none | 150 | 0.997 | 0.997 |
| opensearch | default | w3_s0p5_pos | 150 | 0.987 | 0.987 |

## Qdrant: did ACORN change the hits of the same query?

For each query an arm answered at both settings in one job, whether the hit lists at `default` and at `acorn` were identical.

| arm | layout | identical | different |
|---|---|---|---|
| a3-spicedb | w3_s0p001_neg | 2987 | 13 |
| a3-spicedb | w3_s0p001_none | 2995 | 5 |
| a3-spicedb | w3_s0p001_pos | 2998 | 2 |
| a3-spicedb | w3_s0p01_neg | 2758 | 242 |
| a3-spicedb | w3_s0p01_none | 2507 | 493 |
| a3-spicedb | w3_s0p01_pos | 2381 | 619 |
| a3-spicedb | w3_s0p05_neg | 31 | 869 |
| a3-spicedb | w3_s0p05_none | 141 | 759 |
| a3-spicedb | w3_s0p05_pos | 299 | 601 |
| a3-spicedb | w3_s0p2_neg | 41 | 259 |
| a3-spicedb | w3_s0p2_none | 99 | 201 |
| a3-spicedb | w3_s0p2_pos | 181 | 119 |
| a3-spicedb | w3_s0p5_neg | 150 | 0 |
| a3-spicedb | w3_s0p5_none | 150 | 0 |
| a3-spicedb | w3_s0p5_pos | 150 | 0 |
| a4 | w3_s0p001_neg | 3000 | 0 |
| a4 | w3_s0p001_none | 3000 | 0 |
| a4 | w3_s0p001_pos | 3000 | 0 |
| a4 | w3_s0p01_neg | 2782 | 218 |
| a4 | w3_s0p01_none | 2625 | 375 |
| a4 | w3_s0p01_pos | 2406 | 594 |
| a4 | w3_s0p05_neg | 119 | 2881 |
| a4 | w3_s0p05_none | 455 | 2545 |
| a4 | w3_s0p05_pos | 965 | 2035 |
| a4 | w3_s0p2_neg | 444 | 2556 |
| a4 | w3_s0p2_none | 972 | 2028 |
| a4 | w3_s0p2_pos | 1791 | 1209 |
| a4 | w3_s0p5_neg | 1096 | 1904 |
| a4 | w3_s0p5_none | 1864 | 1136 |
| a4 | w3_s0p5_pos | 2389 | 611 |
